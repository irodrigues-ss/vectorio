#!-*-coding:utf-8-*-

import pytest

from vectorio.vector.wkt.wkt import WKT
from vectorio.vector.exceptions import WKTInvalid


class TestWKTInvalid:

    @classmethod
    def setup_class(cls):
        cls.invalid_data1 = 'POINTS(-48.72097688990726 -8.288651650245413)'
        cls.invalid_data2 = ''
        cls.invalid_data3 = 'ABC'

    def test_datasource(self):
        wkt = WKT()
        with pytest.raises(WKTInvalid):
            wkt.datasource(self.invalid_data1)
            wkt.datasource(self.invalid_data2)
            wkt.datasource(self.invalid_data3)
