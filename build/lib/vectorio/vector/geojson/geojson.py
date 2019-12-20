#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from osgeo.ogr import DataSource, Feature
from osgeo import ogr
from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import GeojsonInvalid
from vectorio.vector._src.generators.generator_geojson import GeneratorGeojson
from vectorio.vector._src.generators.generator_with_feature_processor import (
    GeneratorWithFeatureProcessor
)
from vectorio.vector._src.generators.feature_collection_concatenated import (
    FeatureCollectionConcatenated
)


class Geojson(IVectorData):

    _driver = None

    def __init__(self):
        self._driver = ogr.GetDriverByName('GeoJSON')

    def datasource(self, input_data: str) -> DataSource:
        datasource = self._driver.Open(input_data)
        if datasource is None:
            raise GeojsonInvalid(
                'Invalid geojson data. Plese check if the data is on geojson pattern.'
            )
        return datasource

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return GeneratorGeojson(
            GeneratorWithFeatureProcessor(datasource)
        ).features()

    def collection(self, datasource: DataSource) -> str:
        return FeatureCollectionConcatenated(self.items(datasource))

    def write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        return self._write_by_collection(ds, out_path)
