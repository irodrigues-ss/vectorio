#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from osgeo.ogr import DataSource, Feature
from osgeo import ogr

from vectorio.vector.geo_output.geojson.feature import FeatureGeojson
from vectorio.vector.geo_output.geojson.feature_collection import FeatureCollectionGeojson
from vectorio.vector.geo_output.geojson.geometry import GeometryGeojson
from vectorio.vector.geo_output.geojson.geometry_collection import GeometryCollectionGeojson
from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import GeojsonInvalid
from vectorio.vector._src.generators.feature_collection_concatenated import (
    FeatureCollectionConcatenated
)
from vectorio.config import GDAL_DRIVERS_NAME
from typeguard import typechecked
from typing import Optional


class Geojson:

    _driver = None
    _data: str

    @typechecked
    def __init__(self, data: str):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['GeoJSON'])
        self._data = data

    @typechecked
    def datasource(self) -> DataSource:
        ds = self._driver.Open(self._data)
        if ds is None:
            raise GeojsonInvalid(
                'Invalid geojson data. Plese check if the data is on geojson pattern.'
            )
        return ds

    @typechecked
    def _features(self, ds: DataSource, nmax: int = None) -> Generator[FeatureGeojson, None, None]:
        lyr = ds.GetLayer(0)

        for i, feat in enumerate(lyr):
            yield FeatureGeojson(feat)

            if i + 1 == nmax:
                break

    @typechecked
    def _geometries(self, ds: DataSource, nmax: Optional[int] = None, ) -> Generator[GeometryGeojson, None, None]:
        lyr = ds.GetLayer(0)
        for i, feat in enumerate(lyr):
            yield GeometryGeojson(feat.geometry())

            if i + 1 == nmax:
                break

    @typechecked
    def features(self, nmax: Optional[int] = None, ds: DataSource = None) -> Generator[FeatureGeojson, None, None]:
        if ds is None:
            return self._features(self.datasource(), nmax)
        return self._features(ds, nmax)

    @typechecked
    def geometries(self, nmax: Optional[int] = None, ds: DataSource = None) -> Generator[GeometryGeojson, None, None]:
        if ds is None:
            return self._geometries(self.datasource(), nmax)
        return self._geometries(ds, nmax)

    @typechecked
    def feature_collection(self, nmax: Optional[int] = None, ds: DataSource = None) -> FeatureCollectionGeojson:
        return FeatureCollectionGeojson(self.features(nmax, ds))

    @typechecked
    def geometry_collection(self, nmax: Optional[int] = None, ds: DataSource = None) -> GeometryCollectionGeojson:
        return GeometryCollectionGeojson(self.geometries(nmax, ds))

    # def write(self, ds: DataSource, out_path: str) -> str:
    #     self._validate_basedir(out_path)
    #     return self._write_by_collection(ds, out_path)
