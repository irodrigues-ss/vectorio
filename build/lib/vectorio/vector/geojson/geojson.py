#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from osgeo.ogr import DataSource, Feature
from osgeo import ogr
from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import GeojsonInvalid
from vectorio.vector._src.generators.feature_collection_concatenated import (
    FeatureCollectionConcatenated
)
from vectorio.config import GDAL_DRIVERS_NAME

class Geojson(IVectorData):

    _driver = None

    def __init__(self):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['GeoJSON'])

    def datasource(self, input_data: str) -> DataSource:
        ds = self._driver.Open(input_data)
        if ds is None:
            raise GeojsonInvalid(
                'Invalid geojson data. Plese check if the data is on geojson pattern.'
            )
        return ds

    def items(self, ds: DataSource) -> Generator[str, None, None]:
        lyr = ds.GetLayer(0)
        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            yield json.dumps(
                json.loads(feat.ExportToJson()), ensure_ascii=False
            )

    def collection(self, ds: DataSource) -> str:
        return FeatureCollectionConcatenated(self.items(ds))

    def write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        return self._write_by_collection(ds, out_path)
