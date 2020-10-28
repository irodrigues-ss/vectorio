#!-*-coding:utf-8-*-

from osgeo.ogr import Geometry
from typeguard import typechecked
from vectorio.config import NoneType
from typing import Union


class GeometryWKT(str):

    @typechecked
    def __new__(cls, geom: Union[Geometry, NoneType] = None):
        if geom is None:
            return str.__new__(cls, 'GEOMETRY_EMPTY')
        return str.__new__(cls, geom.ExportToWkt())
