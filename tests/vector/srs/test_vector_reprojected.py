#!-*-coding:utf-8-*-

import os
import json

from tests.config import FILESDIR_FROM_FIXTURES
from vectorio.vector import Shapefile, ShapefileCompressed
from vectorio.compress import Zip
from vectorio.vector import VectorReprojected
from osgeo.ogr import DataSource


class TestVectorReprojected:

    def setup_method(self):
        self.shp_utm_22 = os.path.join(
            FILESDIR_FROM_FIXTURES, 'data_utm22.zip'
        )
        self.shapefile = ShapefileCompressed(Shapefile(self.shp_utm_22), compress_engine=Zip())
        self.vector = VectorReprojected(self.shapefile, out_srid=4674)

    def test_datasource(self):
        ds = self.vector.datasource()
        assert isinstance(ds, DataSource)
        assert ds.GetLayerCount() == 1
        lyr = ds.GetLayer()
        assert lyr.GetFeatureCount() == 1

    def test_features(self):
        ds = self.vector.datasource()
        for item in self.vector.features(ds=ds):  # only one iteration
            item_dict = json.loads(item)
            for pt in item_dict["geometry"]["coordinates"][0]:
                assert int(pt[0]) == -48 and int(pt[1]) == -18

    def test_feature_collection(self):
        ds = self.vector.datasource()
        coll_dict = json.loads(self.vector.feature_collection(ds=ds))
        for feat in coll_dict["features"]:
            for pt in feat["geometry"]["coordinates"][0]:
                assert int(pt[0]) == -48 and int(pt[1]) == -18
