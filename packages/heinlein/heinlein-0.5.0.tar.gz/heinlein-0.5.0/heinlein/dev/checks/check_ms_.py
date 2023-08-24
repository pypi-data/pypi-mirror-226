import astropy.units as u
from astropy.coordinates import SkyCoord

from heinlein import load_dataset

ms = load_dataset("ms")
center = SkyCoord(0, 0, unit="deg")
ms.set_field((0, 2))
