#!-*-coding:utf-8-*-

import os
from vectorio.vector import Shapefile, ShapefileCompressed, VectorReprojected
from tests.config import get_test_file


class TestShapeEncoding:

    def setup_method(self):
        self.shape_latin_path = get_test_file('point-latin.zip')

    def test_from_file(self):
        dt = ShapefileAsZip(VectorReprojected(Shapefile(), out_srid=4674)).datasource(self.shape_latin_path)
        assert os.environ['SHAPE_ENCODING'] == 'ISO-8859-1'
