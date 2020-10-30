#!-*-coding:utf-8-*-

from uuid import uuid4
from osgeo import ogr, osr
from osgeo.ogr import DataSource, Layer
from osgeo.osr import SpatialReference
from vectorio.vector._src.gdal_aux.cloned_feature import GDALClonedFeature
from vectorio.vector._src.gdal_aux.cloned_layer import GDALClonedLayer
from vectorio.vector.exceptions import DataSourceWithoutSpatialRef
from vectorio.config import GDAL_DRIVERS_NAME
from vectorio.vector.srs.srs import SRS


class DataSourceReprojected:

    _inp_ds = None
    _in_srid = None
    _out_srid = None
    _in_wkt_prj = None
    _out_wkt_prj = None
    _use_wkt_prj = None

    def __init__(
        self, inp_ds: DataSource, in_srid=None, out_srid=None,
        in_wkt_prj=None, out_wkt_prj=None, use_wkt_prj=False
    ):
        self._inp_ds = inp_ds
        self._in_srid = in_srid
        self._out_srid = out_srid
        self._in_wkt_prj = in_wkt_prj
        self._out_wkt_prj = out_wkt_prj
        self._use_wkt_prj = use_wkt_prj
        self._driver_mem = ogr.GetDriverByName(GDAL_DRIVERS_NAME['MEMORY'])

    def ref(self):
        inp_lyr = self._inp_ds.GetLayer()
        srs = SRS(
            self._inp_ds.name, inp_lyr, self._in_srid, self._out_srid,
            self._in_wkt_prj, self._out_wkt_prj, self._use_wkt_prj
        )
        coord_transformator = srs.coord_transformator()
        out_ds = self._driver_mem.CreateDataSource(str(uuid4()))
        out_lyr = GDALClonedLayer(out_ds, inp_lyr).ref()
        outLayerDefn = out_lyr.GetLayerDefn()
        in_feature = inp_lyr.GetNextFeature()

        while in_feature:
            geom = in_feature.GetGeometryRef()
            if geom is not None:
                geom.Transform(coord_transformator)
                gdal_feature = GDALClonedFeature(outLayerDefn, geom, in_feature)
                out_lyr.CreateFeature(gdal_feature.ref())
            in_feature = inp_lyr.GetNextFeature()

        inp_lyr.ResetReading()
        out_lyr.ResetReading()
        return out_ds
