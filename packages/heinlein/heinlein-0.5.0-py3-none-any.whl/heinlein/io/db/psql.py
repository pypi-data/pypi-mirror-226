from sqlalchemy import Engine

from heinlein.region.base import BaseRegion
from heinlein.region.region import CircularRegion, PolygonRegion


def region_search(connection: Engine, region: BaseRegion):
    match type(region):
        case CircularRegion():
            return circular_region_search(connection, region)
        case PolygonRegion():
            return polygon_region_search(connection, region)
        

def circular_region_search(connection: Engine, region: CircularRegion):
    pass

def polygon_region_search(connection: Engine, region: PolygonRegion):
    pass