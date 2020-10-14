#!-*-coding:utf-8-*-
import os
from vectorio.vector import KML
from tests.config import FILESDIR_FROM_FIXTURES
from osgeo.ogr import DataSource
from typing import Generator


class TestKML:

    def setup_method(self):
        # self._path = os.path.join(FILESDIR_FROM_FIXTURES, 'test-polygon.kml')
        self._path = os.path.join(FILESDIR_FROM_FIXTURES, 'test2-polygon-point.kml')

    def test_datasource(self):
        kml = KML(self._path)
        assert isinstance(kml.datasource(), DataSource)

    def test_features(self):
        kml = KML(self._path)
        fetures = kml.features()
        assert isinstance(fetures, Generator)

    def test_feature_collection(self):
        kml = KML(self._path)
        NMAX = 1
        assert kml.feature_collection(NMAX) == '{"type": "FeatureCollection","features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-48.27027913600892, -8.186021032258662, 2000.22314031049], [-49.73393654601743, -9.1804358799212, -890.2663457034835], [-47.57679839991549, -9.474809494952101, 930.5758148298509], [-48.27027913600892, -8.186021032258662, 2000.22314031049]]]}, "properties": {"Name": "test", "Description": ""}, "id": 0}]}'

    def test_geometry_collection(self):
        kml = KML(self._path)
        NMAX = 1
        assert kml.geometry_collection(NMAX) == '{"type": "GeometryCollection","geometries": [{ "type": "Polygon", "coordinates": [ [ [ -48.270279136008917, -8.186021032258662, 2000.223140310489953 ], [ -49.733936546017432, -9.1804358799212, -890.266345703483466 ], [ -47.576798399915489, -9.474809494952101, 930.575814829850856 ], [ -48.270279136008917, -8.186021032258662, 2000.223140310489953 ] ] ] }]}'
