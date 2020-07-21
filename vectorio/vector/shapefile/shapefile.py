#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from uuid import uuid4
from osgeo import ogr, osr
from osgeo.ogr import DataSource, Feature
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


class Shapefile(IVectorFile):

    _driver = None
    _shape_encoding = None
    _search_encoding = None
    _srid = None

    def __init__(self, search_encoding=True, search_encoding_exception=True, srid: int=None):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['ESRI Shapefile'])
        self._search_encoding = search_encoding
        self._shape_encoding = ShapeEncodings(
            raise_exception=search_encoding_exception
        )
        self._srid = srid

    def _has_data(self, ds: DataSource):
        lyr = ds.GetLayer()
        if lyr.GetFeature(0) is None:
            raise ShapefileIsEmpty(
                "Shapefile is empty. Please, check if your shapefile has data."
            )

    def datasource(self, fpath: str) -> DataSource:
        if not os.path.exists(fpath):
            raise FileNotFound(f'"{fpath}" does not exists.')

        if self._search_encoding:
            os.environ['SHAPE_ENCODING'] = self._shape_encoding.from_file(
                fpath.replace('.shp', '.dbf')  # getting path from .dbf
            )

        ds = self._driver.Open(fpath)

        if ds is None:
            raise ShapefileInvalid(
                'Shapefile invalid. Please, check if your shapefile is correct'
                ' or if the files .dbf .shx and .prj are next to the .shp file.'
            )
        self._has_data(ds)
        return GDALClonedDataSource(ds).ref()

    def _export_json(self, feat: Feature) -> str:
        return json.dumps(
            json.loads(feat.ExportToJson()), ensure_ascii=False
        )

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        lyr = datasource.GetLayer(0)
        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            yield self._export_json(feat)

    def collection(self, datasource: DataSource) -> str:
        return FeatureCollectionConcatenated(self.items(datasource))

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





