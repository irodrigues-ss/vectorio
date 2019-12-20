#!-*-coding:utf-8-*-

import os
from vectorio.vector import WKT, GeoFile
from osgeo.ogr import DataSource
from osgeo import ogr
from typing import Generator


class TestWKT:

    def setup_method(self):
        self.exp_data_lst = [
            'GEOMETRYCOLLECTION(POLYGON((-51.065799966597524 -8.903757033409324,-47.110721841597524 -8.903757033409324,-47.110721841597524 -13.215577143495809,-51.065799966597524 -13.215577143495809,-51.065799966597524 -8.903757033409324)),POINT(-54.361698404097524 -6.988822067619378))'
            'POINT(-48.72097688990726 -8.288651650245413)'
            'LINESTRING(-58.955235731835955 -1.8197987028528193,-58.955235731835955 -5.503030673351235)'
            'POLYGON((13.109230852463384 29.786738420859706,15.350441789963384 29.17465773736673,11.571144914963384 27.39464289200021,13.109230852463384 29.786738420859706))'
            'MULTIPOLYGON(((14.998879289963384 27.85214109993116,14.910988664963384 27.696611776538724,15.273537493088384 27.754961325572953,14.998879289963384 27.85214109993116)),((15.921730852463384 27.579819092980323,16.009621477463384 27.321461423954766,16.207375383713384 27.609028948315288,15.921730852463384 27.579819092980323)))'
            'MULTILINESTRING((-58.354891141990265 -2.7609863418615888,-58.332918485740265 -3.770074227201964,-58.310945829490265 -4.318020797171471), (-58.955235731835955 -1.8197987028528193,-58.955235731835955 -5.503030673351235))'
            'MULTIPOINT((-47.88601595240726 -8.4625580254647), (-48.72097688990726 -8.288651650245413))'
        ]
        self.wkt_fpath = '/tmp/test.wkt'

    def test_datasource(self):
        wkt = WKT()
        for exp_data in self.exp_data_lst:
            assert isinstance(wkt.datasource(exp_data), DataSource)

    def test_items(self):
        wkt = WKT()

        for exp_data in self.exp_data_lst:
            ds = wkt.datasource(exp_data)
            gen_data = wkt.items(ds)
            assert isinstance(gen_data, Generator)
            for data in gen_data:
                geom = ogr.CreateGeometryFromWkt(data)
                exp_geom = ogr.CreateGeometryFromWkt(exp_data)
                assert exp_geom.ExportToWkt().replace(' ', '') == \
                    geom.ExportToWkt().replace(' ', '')

    def test_collection(self):
        wkt = WKT()
        for exp_data in self.exp_data_lst:
            ds = wkt.datasource(exp_data)
            collection = wkt.collection(ds)
            assert collection.startswith('GEOMETRYCOLLECTION')
            assert collection.count('GEOMETRYCOLLECTION') == 1

    def test_write(self):
        wkt = WKT()
        ds = wkt.datasource(self.exp_data_lst[0])
        fpath = wkt.write(ds, self.wkt_fpath)
        assert os.path.exists(fpath)
        geoc = wkt.collection(GeoFile(wkt).datasource(fpath))
        assert geoc != ''
        assert geoc.startswith('GEOMETRYCOLLECTION')

    def teardown_method(self):
        if os.path.exists(self.wkt_fpath):
            os.remove(self.wkt_fpath)
