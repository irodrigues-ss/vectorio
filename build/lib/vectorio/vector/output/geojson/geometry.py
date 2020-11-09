#!-*-coding:utf-8-*-

from osgeo.ogr import Geometry
from typing import Union
from vectorio.config import NoneType


class GeometryGeojson(str):

    def __new__(cls, geometry: Union[Geometry, NoneType]):
        if geometry is None:
            return None
        return str.__new__(cls, geometry.ExportToJson())
