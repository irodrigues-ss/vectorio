#!-*-coding:utf-8-*-

from typing import Union, Optional
from uuid import uuid4
from osgeo.ogr import DataSource
from typeguard import typechecked, Generator
from osgeo import ogr, osr

from vectorio.config import NoneType
from vectorio.vector.exceptions import KMLInvalid
from vectorio.vector.geojson.geojson import Geojson


class KML(Geojson):

    @typechecked
    def __init__(self, path: Optional[Union[str, NoneType]] = None):
        self._path = path
        self._driver = ogr.GetDriverByName('KML')

    @typechecked
    def source(self) -> Union[str, NoneType]:
        return self._path

    @typechecked
    def datasource(self) -> DataSource:
        ds = self._driver.Open(self._path)
        if ds is None:
            raise KMLInvalid(
                'KML invalid. Please, check if your KML path is correct.'
            )
        return ds
