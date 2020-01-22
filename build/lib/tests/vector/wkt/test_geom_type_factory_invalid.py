#!-*-coding:utf-8-*-

import pytest

from vectorio.vector.wkt.geom_type_factory import (
    GeometryTypeFactory
)
from vectorio.vector.exceptions import GeometryTypeInvalid


class TestGeometryTypeFactoryInvalid:

    @classmethod
    def setup_class(cls):
        cls.geom_type_lst = [
            'GEOMETRYCOLLECTIONS',
            'TESTE',
            'ABC',
        ]

    def test_get_type(self):
        gt_factory = GeometryTypeFactory()

        for geom_type in self.geom_type_lst:
            with pytest.raises(GeometryTypeInvalid):
                gt_factory.get_type(geom_type)
