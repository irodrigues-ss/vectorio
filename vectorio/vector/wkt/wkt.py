#!-*-coding:utf-8-*-

from uuid import uuid4
from typing import Generator
from functools import reduce

from osgeo import ogr, osr
from osgeo.ogr import Geometry, DataSource, Feature

from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import WKTInvalid
from vectorio.vector.wkt.geom_type_factory import GeometryTypeFactory


GEOMETRYCOLLECTION_PREFIX = 'GEOMETRYCOLLECTION'


class WKT(IVectorData):

    _gt_factory = None
    _initial_srid = 0
    _as_geometry_collection = True

    def __init__(self, as_geometry_collection: bool=True, srid: int=4326):
        self._gt_factory = GeometryTypeFactory()
        self._initial_srid = srid
        self._as_geometry_collection = as_geometry_collection

    def _srs(self):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self._initial_srid)
        return srs

    def datasource(self, input_data: str) -> DataSource:
        drv = ogr.GetDriverByName('MEMORY')
        out_ds = drv.CreateDataSource(str(uuid4()))
        geom = None
        if not bool(input_data):
            raise WKTInvalid(
                'Invalid wkt data. Please, check if data is a wkt valid.'
            )

        geom = ogr.CreateGeometryFromWkt(input_data)

        if geom is None:
            raise WKTInvalid(
                f'Invalid wkt data. Please, check is the data "{input_data}" is in wkt pattern.'
            )
        l1 = out_ds.CreateLayer(
            str(uuid4()), self._srs(),
            self._gt_factory.get_type(geom.GetGeometryName())
        )
        feat = ogr.Feature(l1.GetLayerDefn())
        feat.SetGeometry(geom)
        # this change on this layer "l1" will be reflected on "_out_ds"
        l1.SetFeature(feat)
        return out_ds

    def items(self, ds: DataSource) -> Generator[str, None, None]:
        lyr = ds.GetLayer(0)

        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            yield feat.geometry().ExportToWkt()

    def collection(self, ds: DataSource) -> str:
        out_wkt = reduce(
            lambda x,y: x + ',' + y, self.items(ds)
        )
        if out_wkt.startswith(GEOMETRYCOLLECTION_PREFIX):
            return out_wkt
        else:
            if self._as_geometry_collection:
                return f'{GEOMETRYCOLLECTION_PREFIX} ({out_wkt})'
            else:
                return out_wkt

    def write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        return self._write_by_collection(ds, out_path)
