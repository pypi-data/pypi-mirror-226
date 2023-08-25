from silx.utils.deprecation import deprecated_warning

deprecated_warning(
    type_="Module",
    name="tomoscan.unitsytem.electriccurrentsystem",
    reason="dedicated project created",
    replacement="pyunitsystem.electriccurrentsystem",
    since_version="2.0",
)

from pyunitsystem.electriccurrentsystem import *  # noqa F401
