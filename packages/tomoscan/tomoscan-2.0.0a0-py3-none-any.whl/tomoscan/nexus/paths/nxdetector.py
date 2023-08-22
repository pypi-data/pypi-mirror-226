from silx.utils.deprecation import deprecated_warning

deprecated_warning(
    type_="Module",
    name="tomoscan.nexus.paths.nxdetector",
    reason="dedicated project created",
    replacement="nxtomo.paths.nxdetector",
    since_version=2.0,
)

from nxtomo.paths.nxdetector import *  # noqa F401
