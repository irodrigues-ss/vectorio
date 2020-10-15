#!-*-coding:utf-8-*-

from osgeo.ogr import Geometry
from typeguard import typechecked


class GeometryWKT(str):

    @typechecked
    def __new__(cls, geom: Geometry):
        return str.__new__(cls, geom.ExportToWkt())
