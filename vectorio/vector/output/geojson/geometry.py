#!-*-coding:utf-8-*-

from osgeo.ogr import Geometry
from typeguard import typechecked


class GeometryGeojson(str):

    @typechecked
    def __new__(cls, geometry: Geometry):
        return str.__new__(cls, geometry.ExportToJson())