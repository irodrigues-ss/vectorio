#!-*-coding:utf-8-*-

import os


def get_root_project(directory):
    path = os.path.abspath(directory)
    if os.path.isdir(path):
        if "vectorio" in os.listdir(path):
            return path
        else:
            return get_root_project(os.path.dirname(path))
    else:
        return get_root_project(os.path.dirname(path))


ROOT_PROJECT = get_root_project(__file__)
STATIC_DIR = os.path.join(ROOT_PROJECT, 'vectorio', '_assets')
GDAL_DRIVERS_NAME = {
    'MEMORY': 'MEMORY',
    'ESRI Shapefile': 'ESRI Shapefile',
    'GeoJSON': 'GeoJSON'
}

GEOMETRYCOLLECTION_PREFIX = 'GEOMETRYCOLLECTION'
GEOM_COLLECTION_LEN = len(GEOMETRYCOLLECTION_PREFIX)

PRJ_WGS84='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

NoneType = type(None)
