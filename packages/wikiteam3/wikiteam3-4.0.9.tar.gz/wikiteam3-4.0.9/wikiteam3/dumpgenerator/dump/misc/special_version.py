import os

from wikiteam3.dumpgenerator.cli import Delay
from wikiteam3.utils import remove_IP
from wikiteam3.dumpgenerator.config import Config


def save_SpecialVersion(config: Config=None, session=None):
    """Save Special:Version as .html, to preserve extensions details"""

    if os.path.exists("%s/SpecialVersion.html" % (config.path)):
        print("SpecialVersion.html exists, do not overwrite")
    else:
        print("Downloading Special:Version with extensions and other related info")
        r = session.post(
            url=config.index, params={"title": "Special:Version"}, timeout=10
        )
        raw = str(r.text)
        Delay(config=config)
        raw = str(remove_IP(raw=raw))
        with open(
            "%s/SpecialVersion.html" % (config.path), "w", encoding="utf-8"
        ) as outfile:
            outfile.write(str(raw))

