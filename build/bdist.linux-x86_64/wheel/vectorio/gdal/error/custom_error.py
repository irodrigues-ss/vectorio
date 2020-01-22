#!-*-coding:utf-8-*-

from osgeo import gdal


class GDALCustomError:

    def __init__(self):
        self.level = gdal.CE_None
        self.code = 0
        self.msg = ''

    def handler(self, err_level: str, err_no: int, err_msg: str):
        self.level=err_level
        self.code=err_no
        self.msg=err_msg

