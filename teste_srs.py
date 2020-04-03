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
        # out_spatial_ref.ImportFromEPSG(self._out_srid)
        out_spatial_ref.ImportFromWkt(
            'PROJCS["Brazil / Albers Equal Area Conic (WGS84)",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["longitude_of_center",-50.0],PARAMETER["standard_parallel_1",10.0],PARAMETER["standard_parallel_2",-40.0],PARAMETER["latitude_of_center",-25.0],UNIT["Meter",1.0]]'
        )
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
            if geom is not None:
                geom.Transform(coord_transformator)
                gdal_feature = GDALClonedFeature(outLayerDefn, geom, in_feature)
                out_lyr.CreateFeature(gdal_feature.ref())
            in_feature = inp_lyr.GetNextFeature()

        return out_ds


from vectorio.vector import WKT
wkt = WKT()
ds = wkt.datasource('LINESTRING(-47.882930160249096 -15.79721665759788,-47.8822649724134 -15.79513127541869)')
dsn = DataSourceReprojected(ds, 4674, out_srid=1).ref()
lyr = dsn.GetLayer()
feat = lyr.GetFeature(0)
geom = feat.geometry()
import pdb; pdb.set_trace()
print()