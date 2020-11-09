#!-*-coding:utf-8-*-

import os
import json
from osgeo.ogr import DataSource, Feature
from osgeo import ogr

from vectorio.vector.output.geojson.feature import FeatureGeojson
from vectorio.vector.output.geojson.feature_collection import FeatureCollectionGeojson
from vectorio.vector.output.geojson.geometry import GeometryGeojson
from vectorio.vector.output.geojson.geometry_collection import GeometryCollectionGeojson
from vectorio.vector.interfaces.ivectorio import IVectorIO
from vectorio.vector.exceptions import GeojsonInvalid
from vectorio.config import GDAL_DRIVERS_NAME, NoneType
from typeguard import typechecked, Generator
from typing import Optional, Union


class Geojson(IVectorIO):

    _driver = None
    _data: Union[str, dict]

    @typechecked
    def __init__(self, data: Optional[Union[str, dict]] = None):
        self._driver = ogr.GetDriverByName(GDAL_DRIVERS_NAME['GeoJSON'])
        self._data = data

        if isinstance(data, dict):
            self._data = json.dumps(data)

    @typechecked
    def datasource(self) -> DataSource:
        ds = self._driver.Open(self._data)
        if ds is None:
            raise GeojsonInvalid(
                'Invalid geojson data. Plese check if the data is on geojson pattern.'
            )
        return ds

    @typechecked
    def source(self) -> Union[str, dict, NoneType]:
        return self._data

    @typechecked
    def _features(self, ds: DataSource, nmax: Optional[Union[int, NoneType]] = None) -> Generator[FeatureGeojson, None, None]:
        lyr = ds.GetLayer(0)

        for i, feat in enumerate(lyr):
            yield FeatureGeojson(feat)

            if i + 1 == nmax:
                break
        lyr.ResetReading()

    @typechecked
    def _geometries(self, ds: DataSource, nmax: Optional[Union[int, NoneType]] = None) -> Generator[GeometryGeojson, None, None]:
        lyr = ds.GetLayer(0)
        for i, feat in enumerate(lyr):
            yield GeometryGeojson(feat.geometry())

            if i + 1 == nmax:
                break
        lyr.ResetReading()

    @typechecked
    def features(
            self, nmax: Optional[Union[int, NoneType]] = None, ds: Optional[Union[DataSource, NoneType]] = None
    ) -> Generator[FeatureGeojson, None, None]:
        if ds is None:
            return self._features(self.datasource(), nmax)
        return self._features(ds, nmax)

    @typechecked
    def geometries(
            self, nmax: Optional[Union[int, NoneType]] = None, ds: Optional[Union[DataSource, NoneType]] = None
    ) -> Generator[GeometryGeojson, None, None]:
        if ds is None:
            return self._geometries(self.datasource(), nmax)
        return self._geometries(ds, nmax)

    @typechecked
    def feature_collection(
        self,
        nmax: Optional[Union[int, NoneType]] = None,
        ds: Optional[Union[DataSource, NoneType]] = None
    ) -> FeatureCollectionGeojson:
        return FeatureCollectionGeojson(self.features(nmax, ds))

    @typechecked
    def geometry_collection(
            self,
            nmax: Optional[Union[int, NoneType]] = None,
            ds: Optional[Union[DataSource, NoneType]] = None
    ) -> GeometryCollectionGeojson:
        return GeometryCollectionGeojson(self.geometries(nmax, ds))

    @typechecked
    def _write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        with open(out_path, 'w') as f:
            f.write(self.feature_collection(ds=ds))
        return out_path

    @typechecked
    def write(self, out_path: str, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        if ds is None:
            return self._write(self.datasource(), out_path)
        return self._write(ds, out_path)
