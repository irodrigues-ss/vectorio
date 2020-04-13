#!-*-coding:utf-8-*-

from osgeo import ogr
from osgeo.ogr import DataSource
from vectorio.config import GDAL_DRIVERS_NAME

class GDALClonedDataSource:

    _inp_ds = None
    _driver_mem = None
    _LYR_NAME = 'Cloned Layer 01'

    def __init__(self, inp_ds: DataSource):
        self._driver_mem = ogr.GetDriverByName(GDAL_DRIVERS_NAME['MEMORY'])
        self._inp_ds = inp_ds

    def ref(self):
        inp_lyr = self._inp_ds.GetLayer()
        out_ds = self._driver_mem.CreateDataSource('out')
        out_ds.CopyLayer(inp_lyr, self._LYR_NAME)
        return out_ds
