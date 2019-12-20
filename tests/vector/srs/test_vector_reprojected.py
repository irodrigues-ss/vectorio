#!-*-coding:utf-8-*-

import os
import json

from tests.config import FILESDIR_FROM_FIXTURES
from vectorio.vector import Shapefile
from vectorio.vector import VectorReprojected
from osgeo.ogr import DataSource


class TestVectorReprojected:

    def setup_method(self):
        self.shp_utm_22 = os.path.join(
            FILESDIR_FROM_FIXTURES, 'data_utm22.zip'
        )
        self.shapefile = Shapefile()
        self.vector = VectorReprojected(self.shapefile, out_srid=4674)

    def test_datasource(self):
        ds = self.vector.datasource(self.shp_utm_22)
        assert isinstance(ds, DataSource)
        assert ds.GetLayerCount() == 1
        lyr = ds.GetLayer()
        assert lyr.GetFeatureCount() == 1

    def test_items(self):
        ds = self.vector.datasource(self.shp_utm_22)
        for item in self.vector.items(ds):  # only one iteration
            item_dict = json.loads(item)
            for pt in item_dict["geometry"]["coordinates"][0]:
                assert int(pt[0]) == -48 and int(pt[1]) == -18

    def test_collection(self):
        ds = self.vector.datasource(self.shp_utm_22)
        coll_dict = json.loads(self.vector.collection(ds))
        for feat in coll_dict["features"]:
            for pt in feat["geometry"]["coordinates"][0]:
                assert int(pt[0]) == -48 and int(pt[1]) == -18
