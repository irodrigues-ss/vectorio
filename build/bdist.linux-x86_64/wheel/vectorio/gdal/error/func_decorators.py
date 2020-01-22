#!-*-coding:utf-8-*-

from vectorio.gdal.error.custom_error import GDALCustomError
from vectorio.gdal.exceptions import (
    GDALSelfIntersectionGeometry, GDALUnknownException, GDALBadClosedPolygon
)
from osgeo import gdal


KEY_SELF_INTERSECTION = 'Self-intersection'
MSG_BAD_CLOSED_POLYGON = 'IllegalArgumentException: Points of LinearRing do not form a closed linestring'


def gdal_warning_as_exception(inner):

    def func(*args, **kwargs):
        error = GDALCustomError()
        handler = error.handler
        gdal.PushErrorHandler(handler)
        gdal.UseExceptions()

        result = inner(*args, **kwargs)

        if error.level == gdal.CE_None:  # without error
            return result
        if MSG_BAD_CLOSED_POLYGON == error.msg:
            raise GDALBadClosedPolygon(error.msg)
        elif KEY_SELF_INTERSECTION in error.msg:
            raise GDALSelfIntersectionGeometry(error.msg)
        else:
            raise GDALUnknownException(error.msg)

    return func
