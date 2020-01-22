#!-*-coding:utf-8-*-

import os
import tempfile
import shutil
import pytest
import json
from vectorio.vector import (
    Shapefile, ShapefileAsZip, ShapefileAsRar, Geojson
)
from tests.config import FILESDIR_FROM_FIXTURES
from osgeo.ogr import DataSource
from osgeo import ogr
from typing import Generator
from zipfile import ZipFile


class TestShapefileValid:

    def setup_method(self):
        self.shapefile = Shapefile()
        self.shapefile_as_zip = ShapefileAsZip(Shapefile())
        self.shape_valid_as_zippath = os.path.join(
            FILESDIR_FROM_FIXTURES, 'ponto-com-attr-utf8.zip'
        )
        self.dirpath_tmp = tempfile.mkdtemp()
        with ZipFile(self.shape_valid_as_zippath) as zipf:
            zipf.extractall(self.dirpath_tmp)
        self.shppath = os.path.join(
            self.dirpath_tmp, 'ponto-com-attr-utf8.shp'
        )
        self.shape_as_rar = os.path.join(
            FILESDIR_FROM_FIXTURES, 'rar001.rar'
        )
        self.fpath_shp = os.path.join(
            FILESDIR_FROM_FIXTURES, 'data_utm22.shp'
        )
        self.gjs = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {"teste": "áàéãôç"},"geometry": {"type": "Polygon","coordinates": [[[-47.63671875,-11.436955216143177],[-49.5703125,-12.983147716796566],[-45.74707031249999,-12.554563528593656],[-47.63671875,-11.436955216143177]]]}}]}'
        self.out_shp = '/tmp/test.shp'
        self.out_shx = self.out_shp.replace('shp', 'shx')
        self.out_dbf = self.out_shp.replace('shp', 'dbf')
        self.out_prj = self.out_shp.replace('shp', 'prj')

    def test_datasource(self):
        ds = self.shapefile_as_zip.datasource(self.shape_valid_as_zippath)
        assert isinstance(ds, DataSource)

    def test_datasource_from_shp(self):
        self.shapefile.datasource(self.fpath_shp)

    def test_items(self):
        ds = self.shapefile_as_zip.datasource(self.shape_valid_as_zippath)
        drv = ogr.GetDriverByName('ESRI Shapefile')
        datasource = drv.Open(self.shppath)
        lyr_exp = datasource.GetLayer(0)
        features = self.shapefile.items(ds)
        assert isinstance(features, Generator)
        for idx, feat in enumerate(features):
            """
            json.dumps(json.loads(...), ensure_ascii=False) this dumps was
            used to fix gdal's utf8 character reading problem
            """
            assert feat == json.dumps(json.loads(lyr_exp.GetFeature(idx).ExportToJson()), ensure_ascii=False)

    def test_collection(self):
        feat_collec = self.shapefile_as_zip.collection(
            self.shapefile_as_zip.datasource(self.shape_valid_as_zippath)
        )
        drv = ogr.GetDriverByName('GeoJSON')
        assert isinstance(drv.Open(feat_collec), DataSource)

    def test_collection_from_rar(self):
        shape_as_rar = ShapefileAsRar(self.shapefile)
        feat_collec = shape_as_rar.collection(
            shape_as_rar.datasource(self.shape_as_rar)
        )
        drv = ogr.GetDriverByName('GeoJSON')
        assert isinstance(drv.Open(feat_collec), DataSource)

    def test_write(self):
        gj = Geojson()
        out_path = self.shapefile.write(
            gj.datasource(self.gjs), self.out_shp
        )
        assert os.path.exists(out_path)
        assert os.path.exists(self.out_shx)
        assert os.path.exists(self.out_prj)
        assert os.path.exists(self.out_dbf)
        assert "áàéãôç" in self.shapefile.collection(
            self.shapefile.datasource(out_path)
        )

    def teardown_method(self):
        shutil.rmtree(self.dirpath_tmp)
        if os.path.exists(self.out_shp):
            os.remove(self.out_shp)
            os.remove(self.out_shx)
            os.remove(self.out_dbf)
            os.remove(self.out_prj)
