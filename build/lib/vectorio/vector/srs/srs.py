#!-*-coding:utf-8-*-

from vectorio.vector.srs.srid import SRSFromSRID
from vectorio.vector.srs.wkt_prj import SRSFromWKTPRJ
from osgeo.ogr import Layer
from osgeo import osr


class SRS:

    _in_srid = None
    _out_srid = None
    _in_wkt_prj = None
    _out_wkt_prj = None
    _use_wkt_prj = None
    _in_lyr = None

    def __init__(
        self, ds_name: str, in_lyr: Layer, in_srid: int=None, out_srid: int=None,
        in_wkt_prj: str=None, out_wkt_prj: str=None, use_wkt_prj=False
    ):
        self._in_srid = in_srid
        self._out_srid = out_srid
        self._in_wkt_prj = in_wkt_prj
        self._out_wkt_prj = out_wkt_prj
        self._use_wkt_prj = use_wkt_prj
        self._ds_name = ds_name
        self._in_lyr = in_lyr

    def coord_transformator(self):
        srs = None

        if self._use_wkt_prj:
            assert self._out_wkt_prj != None, 'Is required output WKT projection'
            srs = SRSFromWKTPRJ(
                self._ds_name, self._in_lyr, in_wkt_prj=self._in_wkt_prj, out_wkt_prj=self._out_wkt_prj
            )
        else:
            assert self._out_srid != None, 'Is required output SRID'
            srs = SRSFromSRID(
                self._ds_name, self._in_lyr, in_srid=self._in_srid, out_srid=self._out_srid
            )    
        in_srs = srs.input_srs()
        out_srs = srs.output_srs()
        return osr.CoordinateTransformation(in_srs, out_srs)