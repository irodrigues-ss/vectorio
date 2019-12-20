#!-*-coding:utf-8-*-

from osgeo import ogr, osr
from osgeo.ogr import DataSource
from vectorio.vector._src.gdal_aux.cloned_feature import GDALClonedFeature
from vectorio.vector._src.gdal_aux.cloned_layer import GDALClonedLayer
from vectorio.vector.exceptions import DataSourceWithoutSpatialRef
from uuid import uuid4


class DataSourceReprojected:

    _inp_ds = None
    _in_srid = None
    _out_srid = None

    def __init__(
        self, inp_ds: DataSource, in_srid: int=None, out_srid: int=None
    ):
        assert out_srid != None, 'Is required output SRID'
        self._inp_ds = inp_ds
        self._in_srid = in_srid
        self._out_srid = out_srid
        self._driver_mem = ogr.GetDriverByName('MEMORY')

    def _create_coord_transformator(self, lyr):
        in_spatial_ref = None

        if self._in_srid is None:
            # getting spatial ref from datasource
            in_spatial_ref = lyr.GetSpatialRef()

            if in_spatial_ref is None:
                raise DataSourceWithoutSpatialRef(
                    f'The datasource {self._inp_ds.name} not have spatial'
                    ' reference. Plese, use the input SRID.'
                )

        else:
            in_spatial_ref = osr.SpatialReference()
            in_spatial_ref.ImportFromEPSG(self._in_srid)

        out_spatial_ref = osr.SpatialReference()
        out_spatial_ref.ImportFromEPSG(self._out_srid)
        return osr.CoordinateTransformation(in_spatial_ref, out_spatial_ref)

    def ref(self):
        inp_lyr = self._inp_ds.GetLayer()
        coord_transformator = self._create_coord_transformator(inp_lyr)
        out_ds = self._driver_mem.CreateDataSource(str(uuid4()))
        out_lyr = GDALClonedLayer(out_ds, inp_lyr).ref()
        outLayerDefn = out_lyr.GetLayerDefn()
        in_feature = inp_lyr.GetNextFeature()

        while in_feature:
            geom = in_feature.GetGeometryRef()
            geom.Transform(coord_transformator)
            gdal_feature = GDALClonedFeature(outLayerDefn, geom, in_feature)
            out_lyr.CreateFeature(gdal_feature.ref())
            in_feature = inp_lyr.GetNextFeature()

        return out_ds
