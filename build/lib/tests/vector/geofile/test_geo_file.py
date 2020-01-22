#!-*-coding:utf-8-*-

import os

from tests.config import FILESDIR_FROM_FIXTURES
from vectorio.vector import WKT, Geojson, GeoFile
from osgeo.ogr import DataSource


class TestGeoFile:

    @classmethod
    def setup_class(cls):
        cls.geojson_fpath = os.path.join(FILESDIR_FROM_FIXTURES, 'geo.geojson')
        cls.wkt_fpath = os.path.join(FILESDIR_FROM_FIXTURES, 'geo.wkt')

    def test_datasource_wkt(self):
        geofile_wkt = GeoFile(WKT())
        ds = geofile_wkt.datasource(self.wkt_fpath)
        assert isinstance(ds, DataSource)

    def test_datasource_geojson(self):
        geofile_gjs = GeoFile(Geojson())
        ds = geofile_gjs.datasource(self.geojson_fpath)
        assert isinstance(ds, DataSource)
