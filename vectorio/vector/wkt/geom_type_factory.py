#!-*-coding:utf-8-*-

from osgeo import ogr
from vectorio.vector.wkt.interfaces.igeom_type_factory import (
    IGeometryTypeFactory
)
from vectorio.vector.exceptions import WKTInvalid, GeometryTypeInvalid


DATA = {
    'POINT': ogr.wkbPoint,
    'LINESTRING': ogr.wkbLineString,
    'POLYGON': ogr.wkbPolygon,
    'MULTIPOINT': ogr.wkbMultiPoint,
    'MULTILINESTRING': ogr.wkbMultiPoint,
    'MULTIPOINT': ogr.wkbMultiPoint,
    'MULTILINESTRING': ogr.wkbMultiLineString,
    'MULTIPOLYGON': ogr.wkbMultiPolygon,
    'GEOMETRYCOLLECTION': ogr.wkbGeometryCollection,
}


class GeometryTypeFactory(IGeometryTypeFactory):

    def get_type(self, input_geom_type):
        geom_type = DATA.get(input_geom_type)
        if geom_type is None:
            raise GeometryTypeInvalid(
                f'The geometry type "{input_geom_type}" isn\'t registered in this project'
            )
        return geom_type
