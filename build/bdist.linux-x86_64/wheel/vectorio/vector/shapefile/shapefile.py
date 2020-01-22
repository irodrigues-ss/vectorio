#!-*-coding:utf-8-*-

import os
import json
from functools import reduce
from typing import Generator
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
from uuid import uuid4
from vectorio.vector._src.gdal_aux.cloned_ds import (
    GDALClonedDataSource
)

os.environ['SHAPE_ENCODING'] = "UTF-8"


class Shapefile(IVectorFile):

    _driver = None

    def __init__(self):
        self._driver = ogr.GetDriverByName('ESRI Shapefile')

    def _has_data(self, ds: DataSource):
        lyr = ds.GetLayer()
        if lyr.GetFeature(0) is None:
            raise ShapefileIsEmpty(
                "Shapefile is empty. Please, check if your shapefile has data."
            )

    def datasource(self, fpath: str) -> DataSource:
        if not os.path.exists(fpath):
            raise FileNotFound(f'"{fpath}" does not exists.')

        ds = self._driver.Open(fpath)
        if ds is None:
            raise ShapefileInvalid(
                'Shapefile invalid. Please, check if your shapefile is correct'
                ' or if the files .dbf .shx and .prj are next to the .shp file.'
            )
        self._has_data(ds)
        return GDALClonedDataSource(ds).ref()

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        lyr = datasource.GetLayer(0)
        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            yield json.dumps(
                json.loads(feat.ExportToJson()), ensure_ascii=False
            )

    def collection(self, datasource: DataSource) -> str:
        return FeatureCollectionConcatenated(self.items(datasource))

    def _create_prj(self, out_prj: str, feat: Feature):
        srs = feat.geometry().GetSpatialReference()
        with open(out_prj, 'w') as f:
            f.write(srs.ExportToWkt())

    def write(self, ds: DataSource, out_path: str,) -> str:
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
        ds_out.CopyLayer(ds.GetLayer(), str(uuid4()))

        out_prj = out_path.replace('.shp', '.prj')
        if not os.path.exists(out_prj):
           self._create_prj(out_prj, feat)

        ds_out.Destroy()
        return out_path
