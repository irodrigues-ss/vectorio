#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from osgeo import gdal, ogr
from osgeo.ogr import DataSource
from vectorio.vector import VectorComposite, WKT, Geojson


class TestVectorComposite:

    def setup_method(self):
        self.wkt_data = 'POINT(-54.36169 -6.98882)'
        self.exp_coords_wkt = [-54.36169, -6.98882]
        self.gjs_data = json.dumps({"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Point","coordinates": [-49.35058,-7.44962]}}]})
        self.gj_path = '/tmp/test-composite.geojson'

    def test_wkt_to_gjs_geometries(self):
        vector = VectorComposite(WKT(self.wkt_data), Geojson())
        gen_data = vector.geometries()
        exp_geom = ogr.CreateGeometryFromWkt(self.wkt_data)
        assert isinstance(gen_data, Generator)

        for idx, data in enumerate(gen_data):  # geojson
            gjs_ds = gdal.OpenEx(data)
            lyr = gjs_ds.GetLayer(0)
            feat = lyr.GetFeature(idx)
            geom_created = feat.geometry()
            assert geom_created.Equal(exp_geom)

    def test_gjs_to_wkt_items(self):
        vector = VectorComposite(Geojson(self.gjs_data), WKT())
        gen_data = vector.geometries()
        gjs_ds = gdal.OpenEx(self.gjs_data)
        lyr = gjs_ds.GetLayer(0)
        assert isinstance(gen_data, Generator)

        for idx, data in enumerate(gen_data):  # wkt item
            feat = lyr.GetFeature(idx)
            exp_geom = feat.geometry()
            geom_created = ogr.CreateGeometryFromWkt(data)
            assert geom_created.Equal(exp_geom)

    def test_wkt_to_gjs_feature_collection(self):
        vector = VectorComposite(WKT(self.wkt_data), Geojson())
        drv = ogr.GetDriverByName('GeoJSON')
        feat_collec = vector.feature_collection()
        assert isinstance(drv.Open(feat_collec), DataSource)

    def test_gjs_to_wkt_collection(self):
        vector = VectorComposite(Geojson(self.gjs_data), WKT())
        geom_collec = vector.geometry_collection()
        assert geom_collec.startswith('GEOMETRYCOLLECTION')

    def test_write(self):
        vector = VectorComposite(WKT(self.wkt_data), Geojson())
        fpath = vector.write(self.gj_path)
        assert os.path.exists(fpath)
        with open(fpath) as f:
            gj = Geojson(f.read())
            data = gj.feature_collection()
        assert json.loads(data)['features'][0]['geometry'][
           'coordinates'
        ] == self.exp_coords_wkt

    def teardown_method(self):
        if os.path.exists(self.gj_path):
            os.remove(self.gj_path)
