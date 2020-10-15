#!-*-coding:utf-8-*-

from typing import Optional
from osgeo.ogr import DataSource
from typeguard import typechecked, Generator
from osgeo import ogr

from vectorio.vector.geo_output.geojson.feature_collection import FeatureCollectionGeojson
from vectorio.vector.geo_output.geojson.feature import FeatureGeojson
from vectorio.vector.geo_output.geojson.geometry_collection import GeometryCollectionGeojson
from vectorio.vector.geo_output.geojson.geometry import GeometryGeojson


class KML:

    @typechecked
    def __init__(self, path: str = None):
        self._path = path
        self._driver = ogr.GetDriverByName('KML')

    @typechecked
    def datasource(self) -> DataSource:
        ds = self._driver.Open(self._path)
        if ds is None:
            raise Exception('ABC')
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
