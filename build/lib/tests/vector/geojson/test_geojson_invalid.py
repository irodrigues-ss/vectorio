#!-*-coding:utf-8-*-

import pytest

from vectorio.vector.geojson.geojson import Geojson
from vectorio.vector.exceptions import GeojsonInvalid


class TestGeojsonInvalid:

    @classmethod
    def setup_class(cls):
        cls.gj_data_lst = [
            "Teste", ""
        ]

    def test_datasource(self):
        gj = Geojson()
        for inv_data in self.gj_data_lst:
            with pytest.raises(GeojsonInvalid):
                assert gj.datasource(inv_data)
