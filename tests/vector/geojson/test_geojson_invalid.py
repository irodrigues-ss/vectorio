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

        for inv_data in self.gj_data_lst:
            gj = Geojson(inv_data)
            with pytest.raises(GeojsonInvalid):
                assert gj.datasource()
