#!-*-coding:utf-8-*-

import os
import json
from vectorio.vector.geojson.geojson import Geojson
from osgeo.ogr import DataSource
from osgeo import gdal, ogr
from vectorio.vector import GeoFile


class TestGeojsonValid:

    def setup_method(self):
        self.gj_data = json.dumps({"type": "FeatureCollection", "features": [{"type": "Feature","properties": {},"geometry": {"type": "Point","coordinates": [-49.35058,-7.44962]}}]})
        self.gj_fpath = '/tmp/teste.geojson'

    def test_datasource(self):
        gj = Geojson(self.gj_data)
        assert gj.datasource() is not None

    def test_features(self):
        gj = Geojson(self.gj_data)
        gj_ds_exp = gdal.OpenEx(self.gj_data)
        lyr_exp = gj_ds_exp.GetLayer(0)

        for idx, data in enumerate(gj.features()):
            assert data == lyr_exp.GetFeature(idx).ExportToJson()

    def test_geometry_collection(self):
        gj = Geojson(self.gj_data)
        feat_collec = gj.geometry_collection()
        drv = ogr.GetDriverByName('GeoJSON')
        assert isinstance(drv.Open(feat_collec), DataSource)

    # def test_write(self):
    #     gj = Geojson(self.gj_data)
    #     fpath = gj.write(ds, self.gj_fpath)
    #     assert os.path.exists(fpath)
    #     assert gj.collection(GeoFile(gj).datasource(fpath)) != ''
    #
    # def teardown_method(self):
    #     if os.path.exists(self.gj_fpath):
    #         os.remove(self.gj_fpath)
