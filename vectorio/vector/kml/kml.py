
import json
from typing import Optional
from osgeo.ogr import DataSource, Feature, Geometry
from typeguard import typechecked, Generator
from osgeo import ogr
from functools import reduce


class FeatureCollectionGeojson(str):

    def __new__(cls, *args, **kwargs):
        features_gen = args[0]
        concat_features_lbd = lambda x, y: str(x) + ',' + str(y)
        features_str = reduce(concat_features_lbd, features_gen)
        return str.__new__(cls, '{"type": "FeatureCollection","features": [' + features_str + ']}')


class GeometryCollectionGeojson(str):

    def __new__(cls, *args, **kwargs):
        features_gen = args[0]
        concat_features_lbd = lambda x, y: str(x) + ',' + str(y)
        geometries_str = reduce(concat_features_lbd, features_gen)
        return str.__new__(cls, '{"type": "GeometryCollection","geometries": [' + geometries_str + ']}')


class GeometryGeojson(str):

    @typechecked
    def __new__(cls, geometry: Geometry):
        return str.__new__(cls, geometry.ExportToJson())


class FeatureGeojson(str):

    @typechecked
    def __new__(cls, feature: Feature):
        content = json.dumps(
            json.loads(feature.ExportToJson()), ensure_ascii=False
        )
        return str.__new__(cls, content)


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
    def features(self, nmax: int = None) -> Generator[FeatureGeojson, None, None]:
        ds = self.datasource()
        lyr = ds.GetLayer(0)

        for i, feat in enumerate(lyr):
            yield FeatureGeojson(feat)

            if i + 1 == nmax:
                break

    @typechecked
    def geometries(self, nmax: Optional[int] = None) -> Generator[GeometryGeojson, None, None]:
        ds = self.datasource()
        lyr = ds.GetLayer(0)

        for i, feat in enumerate(lyr):
            yield GeometryGeojson(feat.geometry())

            if i + 1 == nmax:
                break

    @typechecked
    def feature_collection(self, nmax: Optional[int] = None) -> FeatureCollectionGeojson:
        return FeatureCollectionGeojson(self.features(nmax))

    @typechecked
    def geometry_collection(self, nmax: Optional[int] = None) -> GeometryCollectionGeojson:
        return GeometryCollectionGeojson(self.geometries(nmax))
