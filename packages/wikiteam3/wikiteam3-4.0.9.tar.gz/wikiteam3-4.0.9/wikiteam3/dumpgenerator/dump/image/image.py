import datetime
import os
from pathlib import Path
import re
import sys
import time
import random
import urllib.parse
from typing import Dict, List, Optional, Union
import warnings

import requests

from wikiteam3.dumpgenerator.api import get_JSON, handle_StatusCode
from wikiteam3.dumpgenerator.cli import Delay
from wikiteam3.dumpgenerator.config import Config, load_config
from wikiteam3.dumpgenerator.dump.image.html_regexs import R_NEXT, REGEX_CANDIDATES
from wikiteam3.dumpgenerator.dump.page.xmlexport.page_xml import get_XML_page
from wikiteam3.dumpgenerator.exceptions import PageMissingError, FileSizeError
from wikiteam3.dumpgenerator.log import log_error
from wikiteam3.utils import url2prefix_from_config, sha1sum, clean_HTML, undo_HTML_entities
from wikiteam3.utils.monkey_patch import SessionMonkeyPatch


NULL = "null"
""" NULL value for image metadata"""


WBM_EARLIEST = 1
WBN_LATEST = 2
WBM_BEST = 3

class Image:
    @staticmethod
    def get_XML_file_desc(config: Config, title="", session=None):
        """Get XML for image description page"""
        warnings.warn("")
        config.curonly = 1  # tricky to get only the most recent desc
        return "".join(
            [
                x
                for x in get_XML_page(
                    config=config, title=title, verbose=False, session=session
                )
            ]
        )


    @staticmethod
    def generate_image_dump(config: Config, other: Dict, images: List[List], session: requests.Session):
        """Save files and descriptions using a file list\n
        Deprecated: `start` is not used anymore."""

        bypass_cdn_image_compression: bool = other["bypass_cdn_image_compression"]
        disable_image_verify: bool = other["disable_image_verify"]
        image_timestamp_interval: str = other["image_timestamp_interval"]
        ia_wbm_booster: int = other["ia_wbm_booster"]

        image_timestamp_intervals = None
        if image_timestamp_interval: # 2019-01-02T01:36:06Z/2023-08-12T10:36:06Z
            image_timestamp_intervals = image_timestamp_interval.split("/")
            assert len(image_timestamp_intervals) == 2
            image_timestamp_intervals = [datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ") for x in image_timestamp_intervals]

        print("Retrieving images...")
        images_dir = Path(config.path) / "images"
        if not os.path.isdir(images_dir):
            print(f'Creating "{images_dir}" directory')
            os.makedirs(images_dir)

        c_savedImageFiles = 0
        c_wbm_speedup_files = 0


        def modify_params(params: Optional[Dict] = None) -> Dict:
            """ bypass Cloudflare Polish (image optimization) """
            if params is None:
                params = {}
            if bypass_cdn_image_compression is True:
                # bypass Cloudflare Polish (image optimization)
                # <https://developers.cloudflare.com/images/polish/>
                params["_wiki_t"] = int(time.time()*1000)
                params[f"_wiki_{random.randint(10,99)}_"] = "random"

            return params
        def check_response(r: requests.Response) -> None:
            assert not r.headers.get("cf-polished", ""), "Found cf-polished header in response, use --bypass-cdn-image-compression to bypass it"
            

        patch_sess = SessionMonkeyPatch(session=session, config=config, hard_retries=3)
        patch_sess.hijack()

        skip_to_filename = '' # TODO: use this
        for filename_raw, original_url, uploader, size, sha1, timestamp in images:
            if skip_to_filename and skip_to_filename != filename_raw:
                print(f"    {filename_raw}", end="\r")
                continue
            else:
                skip_to_filename = ''

            downloaded = False

            if image_timestamp_intervals:
                if timestamp == NULL:
                    print(f"    {filename_raw}|timestamp is unknown: {NULL}, downloading anyway...")
                else:
                    if not (
                        image_timestamp_intervals[0]
                        <= datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                        <= image_timestamp_intervals[1]
                    ):
                        print(f"    timestamp {timestamp} is not in interval {image_timestamp_interval}: {filename_raw}")
                        continue
                    else:
                        print(f"    timestamp {timestamp} is in interval {image_timestamp_interval}: {filename_raw}")

            # saving file
            filename_unquoted = filename_raw # filename_raw is already unquoted
            if filename_unquoted != urllib.parse.unquote(filename_raw):
                print(f"WARNING:    {filename_raw}|filename may not be unquoted: {filename_unquoted}")
            if len(filename_unquoted.encode('utf-8')) > other["filenamelimit"]:
                log_error(
                    config=config, to_stdout=True,
                    text=f"Filename is too long(>{other['filenamelimit']} bytes), skipping: '{filename_unquoted}'",
                )
                # TODO: hash as filename instead of skipping
                continue
            filepath = images_dir / filename_unquoted
            
            # check if file already exists and has the same size and sha1
            if ((size != NULL
                and filepath.is_file()
                and os.path.getsize(filepath) == int(size)
                and sha1sum(filepath) == sha1)
            or (sha1 == NULL and filepath.is_file())): 
            # sha1 is NULL if file not in original wiki (probably deleted,
            # you will get a 404 error if you try to download it)
                c_savedImageFiles += 1
                downloaded = True
                print_msg=f"    {c_savedImageFiles}|sha1 matched: {filename_unquoted}"
                print(print_msg[0:70], end="\r")
                if sha1 == NULL:
                    log_error(config=config, to_stdout=True,
                        text=f"sha1 is {NULL} for {filename_unquoted}, file may not in wiki site (probably deleted). "
                    )
            else:
                # Delay(config=config, delay=config.delay + random.uniform(0, 1))
                url = original_url

                r: Optional[requests.Response] = None
                if ia_wbm_booster:
                    if ia_wbm_booster == WBM_EARLIEST:
                        ia_timestamp = WBM_EARLIEST
                    elif ia_wbm_booster == WBN_LATEST:
                        ia_timestamp = WBN_LATEST
                    elif ia_wbm_booster == WBM_BEST:
                        if timestamp != NULL:
                            ia_timestamp = [x for x in timestamp if x.isdigit()][0:8]
                            ia_timestamp = "".join(ia_timestamp)
                        else:
                            print(f"ia_wbm_booster:    timestamp is {NULL}, use latest timestamp")
                            ia_timestamp = 2
                    else:
                        raise ValueError(f"ia_wbm_booster is {ia_wbm_booster}, but it should be 0, 1, 2 or 3")

                    available_api = "http://archive.org/wayback/available"
                    snap_url = f"https://web.archive.org/web/{ia_timestamp}id_/{url}"

                    try:
                        _r = session.get(available_api, params={"url": url}, headers={"User-Agent": "wikiteam3"},
                                         timeout=10)
                        _r.raise_for_status()
                        api_result = _r.json()
                        if api_result["archived_snapshots"]:
                            r = session.get(url=snap_url, allow_redirects=True)
                            # r.raise_for_status()
                        else:
                            r = None
                    except Exception as e:
                        print("ia_wbm_booster:",e)
                        r = None

                    # verify response
                    if r is not None and r.status_code != 200:
                        r = None
                    elif r is not None and len(r.content) != int(size): # and r.status_code == 200:
                        # FileSizeError
                        # print(f"WARNING:    {filename_unquoted} size should be {size}, but got {len(r.content)} from WBM, use original url...")
                        r = None

                    if r is not None:
                        c_wbm_speedup_files += 1


                if r is None:
                    try:
                        config_dynamic = load_config(config=config, config_filename="config.json")
                    except Exception as e:
                        print(e)
                        config_dynamic = config
                    Delay(config=config, delay=config_dynamic.delay)
                    r = session.get(url=url, params=modify_params(), allow_redirects=True, timeout=15)
                    check_response(r)

                    # Try to fix a broken HTTP to HTTPS redirect
                    original_url_redirected = url != r.url
                    if r.status_code == 404 and original_url_redirected:
                        if (
                            original_url.startswith("http://")
                            and url.startswith("https://")
                        ):
                            url = "https://" + original_url.split("://")[1]
                            # print 'Maybe a broken http to https redirect, trying ', url
                            r = session.get(url=url, params=modify_params(), allow_redirects=True)
                            check_response(r)

                if r.status_code == 200:
                    try:
                        if size == NULL or len(r.content) == int(size) or disable_image_verify:
                            # size == NULL means size is unknown
                            try:
                                with open(filepath, "wb") as imagefile:
                                    imagefile.write(r.content)
                            except KeyboardInterrupt:
                                if filepath.is_file():
                                    os.remove(filepath)
                                raise
                            c_savedImageFiles += 1
                        else:
                            raise FileSizeError(file=filepath, size=size)
                    except OSError:
                        log_error(
                            config=config, to_stdout=True,
                            text=f"File '{filepath}' could not be created by OS",
                        )
                    except FileSizeError as e:
                        # TODO: add a --force-download-image or --nocheck-image-size option to download anyway
                        log_error(
                            config=config, to_stdout=True,
                            text=f"File '{e.file}' size is not match '{e.size}', skipping",
                        )
                else:
                    log_error(
                        config=config, to_stdout=True,
                        text=f"Failled to donwload '{filename_unquoted}' with URL '{url}' due to HTTP '{r.status_code}', skipping"
                    )

            if downloaded: # skip printing
                continue
            print_msg = f"              | {(len(images)-c_savedImageFiles)}=>{filename_unquoted[0:50]}"
            print(print_msg, " "*(73 - len(print_msg)), end="\r")

        patch_sess.release()
        print(f"Downloaded {c_savedImageFiles} files")
        if ia_wbm_booster and c_wbm_speedup_files:
            print(f"(WBM speedup: {c_wbm_speedup_files} files)")


    @staticmethod
    def get_image_names(config: Config, session: requests.Session):
        """Get list of image names"""

        print(")Retrieving image filenames")
        images = []
        if config.api:
            print("Using API to retrieve image names...")
            images = Image.get_image_names_API(config=config, session=session)
        elif config.index:
            print("Using index.php (Special:Imagelist) to retrieve image names...")
            images = Image.get_image_names_scraper(config=config, session=session)

        # images = list(set(images)) # it is a list of lists
        print("Sorting image filenames")
        images.sort()

        print("%d image names loaded" % (len(images)))
        return images


    @staticmethod
    def get_image_names_scraper(config: Config, session: requests.Session):
        """Retrieve file list: filename, url, uploader"""

        images = []
        limit = 5000
        retries = config.retries
        offset = None
        while offset or len(images) == 0:
            # 5000 overload some servers, but it is needed for sites like this with
            # no next links
            # http://www.memoryarchive.org/en/index.php?title=Special:Imagelist&sort=byname&limit=50&wpIlMatch=
            params = {"title": "Special:Imagelist", "limit": limit, "dir": "prev", "offset": offset}
            r = session.post(
                url=config.index,
                params=params,
                timeout=30,
            )
            raw = r.text
            Delay(config=config)
            # delicate wiki
            if re.search(
                r"(?i)(allowed memory size of \d+ bytes exhausted|Call to a member function getURL)",
                raw,
            ):
                if limit > 10:
                    print(f"Error: listing {limit} images in a chunk is not possible, trying tiny chunks")
                    limit = limit // 10
                    continue
                elif retries > 0:  # waste retries, then exit
                    retries -= 1
                    print("Retrying...")
                    continue
                else:
                    raise RuntimeError("retries exhausted")

            raw = clean_HTML(raw)

            # Select the regexp that returns more results
            best_matched = 0
            regexp_best = None
            for regexp in REGEX_CANDIDATES:
                _count = len(re.findall(regexp, raw))
                if _count > best_matched:
                    best_matched = _count
                    regexp_best = regexp
            assert regexp_best is not None, "Could not find a proper regexp to parse the HTML"
            m = re.compile(regexp_best).finditer(raw)

            # Iter the image results
            for i in m:
                url = i.group("url")
                url = Image.curate_image_URL(config=config, url=url)
                filename = re.sub("_", " ", i.group("filename"))
                filename = undo_HTML_entities(text=filename)
                filename = urllib.parse.unquote(filename)
                uploader = re.sub("_", " ", i.group("uploader"))
                uploader = undo_HTML_entities(text=uploader)
                uploader = urllib.parse.unquote(uploader)
                # timestamp = i.group("timestamp")
                # print("    %s" % (timestamp))
                size = NULL # size not accurate
                sha1 = NULL # sha1 not available
                timestamp = NULL # date formats are difficult to parse
                images.append([
                    filename, url, uploader,
                    size, sha1, timestamp,
                ])
                # print (filename, url)

            if re.search(R_NEXT, raw):
                new_offset = re.findall(R_NEXT, raw)[0]
                # Avoid infinite loop
                if new_offset != offset:
                    offset = new_offset
                    retries += 5  # add more retries if we got a page with offset
                else:
                    print("Warning: offset is not changing")
                    offset = ""
            else:
                print("INFO: no next link found, we may have reached the end")
                offset = ""

        if len(images) == 0:
            print("Warning: no images found")
        elif len(images) == limit:
            print(f"Warning: the number of images is equal to the limit parameter ({limit}), there may be more images")
        else:
            print(f"    Found {len(images)} images")

        images.sort()
        return images

    @staticmethod
    def get_image_names_API(config: Config, session: requests.Session):
        """Retrieve file list: filename, url, uploader, size, sha1"""
        oldAPI = False
        # # Commented by @yzqzss:
        # https://www.mediawiki.org/wiki/API:Allpages
        # API:Allpages requires MW >= 1.8 
        # (Note: The documentation says that it requires MediaWiki >= 1.18, but that's not true.)
        # (Read the revision history of [[API:Allpages]] and the source code of MediaWiki, you will
        # know that it's existed since MW 1.8) (2023-05-09)
        # https://www.mediawiki.org/wiki/API:Allimages
        # API:Allimages requires MW >= 1.13

        aifrom = "!"
        images = []
        countImages = 0
        while aifrom:
            print(f'Using API:Allimages to get the list of images, {len(images)} images found so far...', end='\r')
            params = {
                "action": "query",
                "list": "allimages",
                "aiprop": "url|user|size|sha1|timestamp",
                "aifrom": aifrom,
                "format": "json",
                "ailimit": config.api_chunksize,
            }
            # FIXME Handle HTTP Errors HERE
            r = session.get(url=config.api, params=params, timeout=30)
            handle_StatusCode(r)
            jsonimages = get_JSON(r)
            Delay(config=config)

            if "query" in jsonimages:
                countImages += len(jsonimages["query"]["allimages"])
                
                # oldAPI = True
                # break
                # # uncomment to force use API:Allpages generator 
                # # may also can as a fallback if API:Allimages response is wrong

                aifrom = ""
                if (
                    "query-continue" in jsonimages
                    and "allimages" in jsonimages["query-continue"]
                ):
                    if "aicontinue" in jsonimages["query-continue"]["allimages"]:
                        aifrom = jsonimages["query-continue"]["allimages"]["aicontinue"]
                    elif "aifrom" in jsonimages["query-continue"]["allimages"]:
                        aifrom = jsonimages["query-continue"]["allimages"]["aifrom"]
                elif "continue" in jsonimages:
                    if "aicontinue" in jsonimages["continue"]:
                        aifrom = jsonimages["continue"]["aicontinue"]
                    elif "aifrom" in jsonimages["continue"]:
                        aifrom = jsonimages["continue"]["aifrom"]
                print(countImages, aifrom[0:30]+" "*(60-len(aifrom[0:30])),end="\r")

                for image in jsonimages["query"]["allimages"]:
                    image: Dict
                    url = image["url"]
                    url = Image.curate_image_URL(config=config, url=url)
                    # encoding to ascii is needed to work around this horrible bug:
                    # http://bugs.python.org/issue8136
                    # (ascii encoding removed because of the following)
                    #
                    # unquote() no longer supports bytes-like strings
                    # so unicode may require the following workaround:
                    # https://izziswift.com/how-to-unquote-a-urlencoded-unicode-string-in-python/
                    if  (
                        ".wikia." in config.api or ".fandom.com" in config.api
                    ):
                        filename = urllib.parse.unquote(
                            re.sub("_", " ", url.split("/")[-3])
                        )
                    else:
                        filename = urllib.parse.unquote(
                            re.sub("_", " ", url.split("/")[-1])
                        )
                    if "%u" in filename:
                        raise NotImplementedError(
                            "Filename "
                            + filename
                            + " contains unicode. Please file an issue with MediaWiki Scraper."
                        )
                    uploader = re.sub("_", " ", image.get("user", "Unknown"))
                    size: Union[bool,int] = image.get("size", NULL)
                    
                    # size or sha1 is not always available (e.g. https://wiki.mozilla.org/index.php?curid=20675)
                    sha1: Union[bool,str] = image.get("sha1", NULL)
                    timestamp = image.get("timestamp", NULL)
                    images.append([filename, url, uploader, size, sha1, timestamp])
            else:
                oldAPI = True
                break

        if oldAPI:
            print("    API:Allimages not available. Using API:Allpages generator instead.")
            gapfrom = "!"
            images = []
            while gapfrom:
                # Some old APIs doesn't have allimages query
                # In this case use allpages (in nm=6) as generator for imageinfo
                # Example:
                # http://minlingo.wiki-site.com/api.php?action=query&generator=allpages&gapnamespace=6
                # &gaplimit=500&prop=imageinfo&iiprop=user|url&gapfrom=!
                params = {
                    "action": "query",
                    "generator": "allpages",
                    "gapnamespace": 6,
                    "gaplimit": config.api_chunksize, # The value must be between 1 and 500.
                                    # TODO: Is it OK to set it higher, for speed?
                    "gapfrom": gapfrom,
                    "prop": "imageinfo",
                    "iiprop": "url|user|size|sha1|timestamp",
                    "format": "json",
                }
                # FIXME Handle HTTP Errors HERE
                r = session.get(url=config.api, params=params, timeout=30)
                handle_StatusCode(r)
                jsonimages = get_JSON(r)
                Delay(config=config)

                if "query" in jsonimages:
                    countImages += len(jsonimages["query"]["pages"])
                    print(countImages, gapfrom[0:30]+" "*(60-len(gapfrom[0:30])),end="\r")

                    gapfrom = ""

                    # all moden(at 20221231) wikis return 'continue' instead of 'query-continue'
                    if (
                        "continue" in jsonimages
                        and "gapcontinue" in jsonimages["continue"]
                    ):
                        gapfrom = jsonimages["continue"]["gapcontinue"]
                    
                    # legacy code, not sure if it's still needed by some old wikis
                    elif (
                        "query-continue" in jsonimages
                        and "allpages" in jsonimages["query-continue"]
                    ):
                        if "gapfrom" in jsonimages["query-continue"]["allpages"]:
                            gapfrom = jsonimages["query-continue"]["allpages"][
                                "gapfrom"
                            ]


                    # print (gapfrom)
                    # print (jsonimages['query'])

                    for image, props in jsonimages["query"]["pages"].items():
                        url = props["imageinfo"][0]["url"]
                        url = Image.curate_image_URL(config=config, url=url)

                        tmp_filename = ":".join(props["title"].split(":")[1:])

                        filename = re.sub("_", " ", tmp_filename)
                        uploader = re.sub("_", " ", props["imageinfo"][0]["user"])
                        size = props.get("imageinfo")[0].get("size", NULL)
                        sha1 = props.get("imageinfo")[0].get("sha1", NULL)
                        timestamp = props.get("imageinfo")[0].get("timestamp", NULL)
                        images.append([filename, url, uploader, size, sha1, timestamp])
                else:
                    # if the API doesn't return query data, then we're done
                    break

        if len(images) == 1:
            print("    Found 1 image")
        else:
            print("    Found %d images" % (len(images)))

        return images


    @staticmethod
    def save_image_names(config: Config, images: List[List]):
        """Save image list in a file, including filename, url, uploader, size and sha1"""

        images_filename = "{}-{}-images.txt".format(
            url2prefix_from_config(config=config), config.date
        )
        images_file = open(
            "{}/{}".format(config.path, images_filename), "w", encoding="utf-8"
        )
        for line in images:
            while 3 <= len(line) < 6:
                line.append(NULL) # At this point, make sure all lines have 5 elements
            filename, url, uploader, size, sha1, timestamp = line
            print(line,end='\r')
            images_file.write(
                filename + "\t" + url + "\t" + uploader
                + "\t" + (str(size) if size else NULL)
                + "\t" + (str(sha1) if sha1 else NULL) # sha1 or size may be NULL
                + "\t" + (timestamp if timestamp else NULL)
                + "\n"
            )
        images_file.write("--END--")
        images_file.close()

        print("Image filenames and URLs saved at...", images_filename)


    @staticmethod
    def curate_image_URL(config: Config, url: str):
        """Returns an absolute URL for an image, adding the domain if missing"""

        if config.index:
            # remove from :// (http or https) until the first / after domain
            domainalone = (
                config.index.split("://")[0]
                + "://"
                + config.index.split("://")[1].split("/")[0]
            )
        elif  config.api:
            domainalone = (
                config.api.split("://")[0]
                + "://"
                + config.api.split("://")[1].split("/")[0]
            )
        else:
            print("ERROR: no index nor API")
            sys.exit(1)

        if url.startswith("//"):  # Orain wikifarm returns URLs starting with //
            url = "{}:{}".format(domainalone.split("://")[0], url)
        # is it a relative URL?
        elif url[0] == "/" or (
            not url.startswith("http://") and not url.startswith("https://")
        ):
            if url[0] == "/":  # slash is added later
                url = url[1:]
            # concat http(s) + domain + relative url
            url = f"{domainalone}/{url}"
        url = undo_HTML_entities(text=url)
        # url = urllib.parse.unquote(url) #do not use unquote with url, it break some
        # urls with odd chars
        url = re.sub(" ", "_", url)

        return url
