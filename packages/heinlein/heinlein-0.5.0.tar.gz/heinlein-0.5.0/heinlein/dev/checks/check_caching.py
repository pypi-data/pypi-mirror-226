import multiprocessing as mp
import time
from functools import partial

import astropy.units as u
from astropy.coordinates import SkyCoord

from heinlein import Region, load_dataset
