#!-*-coding:utf-8-*-

import os
from tests.config import FILESDIR_FROM_FIXTURES
from vectorio.vector import Shapefile
from vectorio.vector import DataSourceReprojected
from vectorio.vector import ShapefileAsZip


class TestDataSourceReprojected:

    def setup_method(self):
        self.shp_utm_22 = os.path.join(
            FILESDIR_FROM_FIXTURES, 'data_utm22.zip'
        )
        self.shapefile = ShapefileAsZip(Shapefile())

    def test_ref(self):
        ds_as_utm22 = self.shapefile.datasource(self.shp_utm_22)
        dsr = DataSourceReprojected(ds_as_utm22, out_srid=4674).ref()
        assert dsr.GetLayerCount() == 1
        lyr = dsr.GetLayer()
        assert lyr.GetFeatureCount() == 1
        feat = lyr.GetFeature(0)
        geom = feat.geometry().GetGeometryRef(0)
        for idx in range(geom.GetPointCount()):
            pt = geom.GetPoint(idx)
            assert int(pt[0]) == -48 and int(pt[1]) == -18
