
#!-*-coding:utf-8-*-

from vectorio.vector.srs.isrs import ISRS
from osgeo.osr import SpatialReference
from osgeo.ogr import Layer
from vectorio.vector.exceptions import WKTPRJNotFound
from osgeo import osr


class SRSFromWKTPRJ(ISRS):

    def __init__(self, ds_name: str, in_lyr: Layer, out_wkt_prj: str, in_wkt_prj=None):
        self._out_wkt_prj = out_wkt_prj
        self._in_wkt_prj = in_wkt_prj
        self._ds_name = ds_name
        self._in_lyr = in_lyr
    
    def input_srs(self) -> SpatialReference:
        if self._in_wkt_prj is None:
            in_spatial_ref = self._srs_from_layer(self._in_lyr, self._ds_name)
        else:
            in_spatial_ref = osr.SpatialReference()
            import_res = in_spatial_ref.ImportFromWkt(self._in_wkt_prj)
            
            if import_res != 0:
                raise WKTPRJNotFound(f'WKT PRJ  "{self._in_wkt_prj}" not found in EPSG support files. This projection is invalid.')
        return in_spatial_ref

    def output_srs(self) -> SpatialReference:
        out_spatial_ref = osr.SpatialReference()
        out_spatial_ref.ImportFromWkt(self._out_wkt_prj)
        return out_spatial_ref