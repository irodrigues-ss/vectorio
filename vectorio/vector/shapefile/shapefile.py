#!-*-coding:utf-8-*-

import os
from uuid import uuid4
from osgeo import ogr, osr
from osgeo.ogr import DataSource, Feature

from vectorio.vector.geojson.geojson import Geojson
from vectorio.vector.exceptions import (
    ShapefileInvalid, ShapefileIsEmpty,
    ImpossibleCreateShapefileFromGeometryCollection, FileNotFound, ShapefilePathWasntPassed
)
from vectorio.vector._src.gdal_aux.cloned_ds import (
    GDALClonedDataSource
)
from vectorio.vector.shapefile.encodings import ShapeEncodings
from vectorio.config import GDAL_DRIVERS_NAME, NoneType
from osgeo import osr
from typing import Optional, Union
from typeguard import typechecked


class Shapefile(Geojson):

    _driver = None
    _shape_encoding: bool
    _search_encoding: bool
    _path: str

    # TODO: add srid in documentation
    @typechecked
    def __init__(
        self, path: Optional[str] = None, search_encoding: bool = False,
        search_encoding_exception: bool = True, srid_for_write: int = 4326
    ):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['ESRI Shapefile'])
        self._search_encoding = search_encoding
        self._search_encoding_exception = search_encoding_exception
        self._shape_encoding = ShapeEncodings(
            raise_exception=search_encoding_exception
        )
        self._path = path
        self._srid_for_write = srid_for_write

    @typechecked
    def source(self) -> Union[str, NoneType]:
        return self._path

    @typechecked
    def _has_data(self, ds: DataSource):
        lyr = ds.GetLayer()
        if lyr.GetFeature(0) is None:
            raise ShapefileIsEmpty(
                "Shapefile is empty. Please, check if your shapefile has data."
            )

    @typechecked
    def _datasource(self, path: Union[str, NoneType]) -> DataSource:
        if path is None:
            raise ShapefilePathWasntPassed("the shapefile path wasn't passed. The path value is None.")

        if not os.path.exists(path):
            raise FileNotFound(f'"{path}" does not exists.')

        if self._search_encoding:
            os.environ['SHAPE_ENCODING'] = self._shape_encoding.from_file(
                path.replace('.shp', '.dbf')  # getting path from .dbf
                # TODO: Change this way for get .dbf path
            )
        ds = self._driver.Open(path)

        if ds is None:
            raise ShapefileInvalid(
                'Shapefile invalid. Please, check if your shapefile is correct'
                ' or if the files .dbf .shx and .prj are next to the .shp file.'
            )
        self._has_data(ds)
        return GDALClonedDataSource(ds).ref()

    @typechecked
    def datasource(self, path: Optional[Union[str, NoneType]] = None) -> DataSource:
        if path is None:
            return self._datasource(self._path)
        return self._datasource(path)

    @typechecked
    def _write(self, ds: DataSource, out_path: str) -> str:
        assert out_path.endswith('.shp'), 'Output file have has .shp extension.'
        lyr = ds.GetLayer()
        feat = lyr.GetFeature(0)

        if feat.geometry().GetGeometryName() == 'GEOMETRYCOLLECTION':
            raise ImpossibleCreateShapefileFromGeometryCollection(
                'Impossible create shapefile from a geometry collection.'
                ' Please, convert the geometry collection for feature '
                'collection with same geometry type.'
            )
        ds_out = self._driver.CreateDataSource(out_path)
        inp_lyr = ds.GetLayer()

        # Configuring projection
        proj = osr.SpatialReference()
        proj.SetWellKnownGeogCS(f'EPSG:{self._srid_for_write}')
        layer_out = ds_out.CreateLayer(str(uuid4()), srs=proj)

        # Configuring attributes
        lyr_def = inp_lyr.GetLayerDefn()
        for i in range(lyr_def.GetFieldCount()):
            layer_out.CreateField(lyr_def.GetFieldDefn(i))

        # Configuring features (with geometries)
        for feat in inp_lyr:
            layer_out.CreateFeature(feat)

        ds_out.Destroy()
        return out_path

    @typechecked
    def write(self, out_path: str, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        if ds is None:
            return self._write(self.datasource(), out_path)
        return self._write(ds, out_path)