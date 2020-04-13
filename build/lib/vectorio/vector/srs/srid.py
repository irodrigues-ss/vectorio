#!-*-coding:utf-8-*-

from vectorio.vector.srs.isrs import ISRS
from osgeo.osr import SpatialReference
from osgeo.ogr import Layer
from vectorio.vector.exceptions import SRIDNotFound
from osgeo import osr


class SRSFromSRID(ISRS):

    def __init__(self, ds_name: str, in_lyr: Layer, out_srid: int, in_srid=None):
        self._out_srid = out_srid
        self._in_srid = in_srid
        self._ds_name = ds_name
        self._in_lyr = in_lyr

    def input_srs(self) -> SpatialReference:
        if self._in_srid is None:
            in_spatial_ref = self._srs_from_layer(self._in_lyr, self._ds_name)
        else:
            in_spatial_ref = osr.SpatialReference()
            import_res = in_spatial_ref.ImportFromEPSG(self._in_srid)
            if import_res != 0:
                raise SRIDNotFound(f'ESPG code {self._in_srid} not found in EPSG support files. This EPSG is invalid.')
        return in_spatial_ref

    def output_srs(self) -> SpatialReference:
        out_spatial_ref = osr.SpatialReference()
        out_spatial_ref.ImportFromEPSG(self._out_srid)
        return out_spatial_ref