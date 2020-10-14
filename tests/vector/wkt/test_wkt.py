#!-*-coding:utf-8-*-

import os
from vectorio.vector import WKT, GeoFile
from osgeo.ogr import DataSource
from osgeo import ogr
from typing import Generator


class TestWKTValid:

    def setup_method(self):
        self.exp_data_lst = [
            'GEOMETRYCOLLECTION(POLYGON((-51.065799966597524 -8.903757033409324,-47.110721841597524 -8.903757033409324,-47.110721841597524 -13.215577143495809,-51.065799966597524 -13.215577143495809,-51.065799966597524 -8.903757033409324)),POINT(-54.361698404097524 -6.988822067619378))',
            'POINT(-48.72097688990726 -8.288651650245413)',
            'LINESTRING(-58.955235731835955 -1.8197987028528193,-58.955235731835955 -5.503030673351235)',
            'POLYGON((13.109230852463384 29.786738420859706,15.350441789963384 29.17465773736673,11.571144914963384 27.39464289200021,13.109230852463384 29.786738420859706))',
            'MULTIPOLYGON(((14.998879289963384 27.85214109993116,14.910988664963384 27.696611776538724,15.273537493088384 27.754961325572953,14.998879289963384 27.85214109993116)),((15.921730852463384 27.579819092980323,16.009621477463384 27.321461423954766,16.207375383713384 27.609028948315288,15.921730852463384 27.579819092980323)))',
            'MULTILINESTRING((-58.354891141990265 -2.7609863418615888,-58.332918485740265 -3.770074227201964,-58.310945829490265 -4.318020797171471), (-58.955235731835955 -1.8197987028528193,-58.955235731835955 -5.503030673351235))',
            'MULTIPOINT((-47.88601595240726 -8.4625580254647), (-48.72097688990726 -8.288651650245413))'
        ]
        self.wkt_fpath = '/tmp/test.wkt'

    def test_datasource(self):
        for exp_data in self.exp_data_lst:
            wkt = WKT(exp_data)
            assert isinstance(wkt.datasource(), DataSource)

    # def test_geometries(self):
    #
    #     def create_items(idx_data: int):
    #         result = []
    #         wkt = WKT(self.exp_data_lst[idx_data])
    #         for geom in wkt.geometries():
    #             result.append(geom)
    #         return result
    #
    #     items = create_items(0)
    #     assert items[0].startswith('GEOMETRYCOLLECTION')
    #     items1 = create_items(1)
    #     assert items1[0].startswith('POINT')
    #     items2 = create_items(2)
    #     assert items2[0].startswith('LINESTRING')
    #     items3 = create_items(3)
    #     assert items3[0].startswith('POLYGON')
    #     items4 = create_items(4)
    #     assert items4[0].startswith('MULTIPOLYGON')
    #     items5 = create_items(5)
    #     assert items5[0].startswith('MULTILINESTRING')
    #     items6 = create_items(6)
    #     assert items6[0].startswith('MULTIPOINT')

    def test_geometry_collection(self):
        for exp_data in self.exp_data_lst:
            wkt = WKT(exp_data)
            geom_collection = wkt.geometry_collection()
            assert geom_collection.startswith('GEOMETRYCOLLECTION')
            assert geom_collection.count('GEOMETRYCOLLECTION') == 1

    def test_geometry_collection(self):
        wkt = WKT(self.exp_data_lst[0])
        assert wkt.geometry_collection().startswith('GEOMETRYCOLLECTION')
        wkt = WKT(self.exp_data_lst[1], as_geometry_collection=False)
        assert wkt.geometry_collection().startswith('POINT')

    def test_geometry_collection_nmax(self):
        wkt = WKT(self.exp_data_lst[0])
        assert wkt.geometry_collection(1) == 'GEOMETRYCOLLECTION (POLYGON ((-51.0657999665975 -8.90375703340932,-47.1107218415975 -8.90375703340932,-47.1107218415975 -13.2155771434958,-51.0657999665975 -13.2155771434958,-51.0657999665975 -8.90375703340932)))'

    def test_collection_param_srid(self):
        srid = 4674
        wkt = WKT(self.exp_data_lst[0], srid=srid)
        ds = wkt.datasource()
        lyr = ds.GetLayer(0)
        feat = lyr.GetFeature(0)
        srs = feat.geometry().GetSpatialReference()
        srs.AutoIdentifyEPSG()
        assert srs.GetAuthorityCode(None) == str(srid)

    # def test_write(self):
    #     wkt = WKT()
    #     ds = wkt.datasource(self.exp_data_lst[0])
    #     fpath = wkt.write(ds, self.wkt_fpath)
    #     assert os.path.exists(fpath)
    #     geoc = wkt.collection(GeoFile(wkt).datasource(fpath))
    #     assert geoc != ''
    #     assert geoc.startswith('GEOMETRYCOLLECTION')
    #
    # def teardown_method(self):
    #     if os.path.exists(self.wkt_fpath):
    #         os.remove(self.wkt_fpath)
