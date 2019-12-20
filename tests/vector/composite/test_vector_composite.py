#!-*-coding:utf-8-*-

import os
import json
from typing import Generator
from osgeo import gdal, ogr
from osgeo.ogr import DataSource
from vectorio.vector import VectorComposite, WKT, Geojson, GeoFile


class TestVectorComposite:

    def setup_method(self):
        self.wkt_data = 'POINT(-54.36169 -6.98882)'
        self.exp_coords_wkt = [-54.36169, -6.98882]
        self.gjs_data = json.dumps({"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Point","coordinates": [-49.35058,-7.44962]}}]})
        self.gj_path = '/tmp/test-composite.geojson'

    def test_wkt_to_gjs_items(self):
        vector = VectorComposite(WKT(), Geojson())
        gen_data = vector.items(self.wkt_data)
        exp_geom = ogr.CreateGeometryFromWkt(self.wkt_data)
        assert isinstance(gen_data, Generator)

        for idx, data in enumerate(gen_data):  # geojson
            gjs_ds = gdal.OpenEx(data)
            lyr = gjs_ds.GetLayer(0)
            feat = lyr.GetFeature(idx)
            geom_created = feat.geometry()
            assert geom_created.Equal(exp_geom)

    def test_gjs_to_wkt_items(self):
        vector = VectorComposite(Geojson(), WKT())
        gen_data = vector.items(self.gjs_data)
        gjs_ds = gdal.OpenEx(self.gjs_data)
        lyr = gjs_ds.GetLayer(0)
        assert isinstance(gen_data, Generator)

        for idx, data in enumerate(gen_data):  # wkt item
            feat = lyr.GetFeature(idx)
            exp_geom = feat.geometry()
            geom_created = ogr.CreateGeometryFromWkt(data)
            assert geom_created.Equal(exp_geom)

    def test_wkt_to_gjs_collection(self):
        vector = VectorComposite(WKT(), Geojson())
        drv = ogr.GetDriverByName('GeoJSON')
        feat_collec = vector.collection(self.wkt_data)
        assert isinstance(drv.Open(feat_collec), DataSource)

    def test_gjs_to_wkt_collection(self):
        vector = VectorComposite(Geojson(), WKT())
        geom_collec = vector.collection(self.gjs_data)
        assert geom_collec.startswith('GEOMETRYCOLLECTION')

    def test_write(self):
        gj = Geojson()
        vector = VectorComposite(WKT(), gj)
        fpath = vector.write(self.wkt_data, self.gj_path)
        assert os.path.exists(fpath)
        data = gj.collection(GeoFile(gj).datasource(fpath))
        assert json.loads(data)['features'][0]['geometry'][
            'coordinates'
        ] == self.exp_coords_wkt

    def teardown_method(self):
        if os.path.exists(self.gj_path):
            os.remove(self.gj_path)
