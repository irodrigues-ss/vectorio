#!-*-coding:utf-8-*-

import os
import tempfile
import shutil
import pytest

from vectorio.vector import Shapefile, ShapefileAsZip, WKT
from tests.config import FILESDIR_FROM_FIXTURES
from zipfile import ZipFile
from vectorio.vector.exceptions import (
    FileNotFound, ImpossibleCreateShapefileFromGeometryCollection
)


class TestShapefileInvalid:

    def setup_method(self):
        self.shapefile = ShapefileAsZip(Shapefile())
        self.shape_invalid_as_zippath = os.path.join(
            FILESDIR_FROM_FIXTURES,
            'ponto-com-attr-utf8-without-shp.zip'
        )
        self.dirpath_tmp = tempfile.mkdtemp()
        with ZipFile(self.shape_invalid_as_zippath) as zipf:
            zipf.extractall(self.dirpath_tmp)
        self.shppath = os.path.join(
            self.dirpath_tmp, 'ponto-com-attr-utf8.shp'
        )
        self.gc_coll = 'GEOMETRYCOLLECTION(POINT(-54.199556902314725 -12.864274888693865), LINESTRING(-54.639010027314725 -16.01306647548315,-53.584322527314725 -14.14615006452015))'

    def test_datasource(self):
        with pytest.raises(FileNotFound):
            self.shapefile.datasource(self.shape_invalid_as_zippath)

    def test_write_error(self):
        wkt = WKT()
        with pytest.raises(ImpossibleCreateShapefileFromGeometryCollection):
            self.shapefile.write(
                wkt.datasource(self.gc_coll), '/tmp/test-invalid.shp'
            )

    def teardown_method(self):
        shutil.rmtree(self.dirpath_tmp)
