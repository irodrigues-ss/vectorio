#!-*-coding:utf-8-*-

from vectorio.vector.wkt.geom_type_factory import (
    GeometryTypeFactory
)
from osgeo import ogr


class TestGeometryTypeFactory:

    @classmethod
    def setup_class(cls):
        cls.geom_type_lst = [
            'GEOMETRYCOLLECTION',
            'POINT',
            'LINESTRING',
            'POLYGON',
            'MULTIPOINT',
            'MULTILINESTRING',
            'MULTIPOLYGON'
        ]
        cls.result_lst = [
            ogr.wkbGeometryCollection,
            ogr.wkbPoint,
            ogr.wkbLineString,
            ogr.wkbPolygon,
            ogr.wkbMultiPoint,
            ogr.wkbMultiLineString,
            ogr.wkbMultiPolygon,
        ]

    def test_get_type(self):
        gt_factory = GeometryTypeFactory()
        for geom_type, geom_exp in zip(self.geom_type_lst, self.result_lst):
            assert gt_factory.get_type(geom_type) == geom_exp
