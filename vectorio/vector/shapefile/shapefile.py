#!-*-coding:utf-8-*-

import os
from uuid import uuid4
from osgeo import ogr, osr
from osgeo.ogr import DataSource, Feature

from vectorio.vector.geojson.geojson import Geojson
from vectorio.vector.interfaces.ivector_file import IVectorFile
from vectorio.vector._src.generators.feature_collection_concatenated import (
    FeatureCollectionConcatenated
)
from vectorio.vector.exceptions import (
    ShapefileInvalid, ShapefileIsEmpty,
    ImpossibleCreateShapefileFromGeometryCollection, FileNotFound
)
from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
from vectorio.vector._src.gdal_aux.cloned_ds import (
    GDALClonedDataSource
)
from vectorio.vector.shapefile.encodings import ShapeEncodings
from vectorio.config import GDAL_DRIVERS_NAME
from osgeo import osr
from typing import Optional, Union
from typeguard import typechecked

NoneType = type(None)

class ShapefilePathWasntPassed(Exception):
    pass


class Shapefile(Geojson):

    _driver = None
    _shape_encoding: bool
    _search_encoding: bool
    _srid: int
    _path: str

    # TODO: add srid in documentation
    @typechecked
    def __init__(
        self, path: Optional[str] = None, search_encoding: bool = True,
        search_encoding_exception: bool =True, srid: Optional[int]=None
    ):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['ESRI Shapefile'])
        self._search_encoding = search_encoding
        self._search_encoding_exception = search_encoding_exception
        self._shape_encoding = ShapeEncodings(
            raise_exception=search_encoding_exception
        )
        self._srid = srid
        self._path = path

    @typechecked
    def path(self) -> Union[str, NoneType]:
        return self._path

    def _has_data(self, ds: DataSource):
        lyr = ds.GetLayer()
        if lyr.GetFeature(0) is None:
            raise ShapefileIsEmpty(
                "Shapefile is empty. Please, check if your shapefile has data."
            )

    def _datasource(self, path: str) -> DataSource:
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
    def datasource(self, path: Optional[str] = None) -> DataSource:
        if path is None:
            return self._datasource(self._path)
        return self._datasource(path)

    # def _create_prj(self, out_prj: str, feat: Feature, srid: int):
    #     srs = feat.geometry().GetSpatialReference()
    #     with open(out_prj, 'w') as f:
    #         f.write(srs.ExportToWkt())

    def write(self, ds: DataSource, out_path: str) -> str:
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
        proj = osr.SpatialReference()
        proj.SetWellKnownGeogCS(f'EPSG:{self._srid}')
        layer_out = ds_out.CreateLayer(str(uuid4()), srs=proj)

        for feat in inp_lyr:
            layer_out.CreateFeature(feat)

        ds_out.Destroy()
        return out_path
