#!-*-coding:utf-8-*-

from uuid import uuid4
from typing import Generator
from functools import reduce

from osgeo import ogr, osr
from osgeo.ogr import Geometry, DataSource, Feature

from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import WKTInvalid
from vectorio.vector.wkt.geom_type_factory import GeometryTypeFactory
from vectorio.config import GDAL_DRIVERS_NAME
from typeguard import typechecked
from typing import Union

GEOMETRYCOLLECTION_PREFIX = 'GEOMETRYCOLLECTION'
GEOM_COLLECTION_LEN = len(GEOMETRYCOLLECTION_PREFIX)



class InvalidOperationForThisDataType(Exception):
    pass


class GeometryWKT(str):

    @typechecked
    def __new__(cls, geom: Geometry):
        return str.__new__(cls, geom.ExportToWkt())


class GeometryCollectionWKT(str):

    @typechecked
    def __new__(cls, wkt_str: str):
        return str.__new__(cls, f'{GEOMETRYCOLLECTION_PREFIX} ({wkt_str})')


class WKT:

    _gt_factory: GeometryTypeFactory
    _initial_srid: int
    _as_geometry_collection: bool
    _data: str

    def __init__(self, data: str, as_geometry_collection=True, srid=4326):
        self._gt_factory = GeometryTypeFactory()
        self._data = data
        self._initial_srid = srid
        self._as_geometry_collection = as_geometry_collection

    def _srs(self):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self._initial_srid)
        return srs

    def _is_geometry_collection(self, geom: Geometry) -> bool:
       return geom.ExportToWkt()[:GEOM_COLLECTION_LEN].startswith(GEOMETRYCOLLECTION_PREFIX)

    def datasource(self) -> DataSource:
        drv = ogr.GetDriverByName(GDAL_DRIVERS_NAME['MEMORY'])
        out_ds = drv.CreateDataSource(str(uuid4()))

        if not bool(self._data):
            raise WKTInvalid(
                'Invalid wkt data. Please, check if data is a wkt valid.'
            )
        geom = ogr.CreateGeometryFromWkt(self._data)

        if geom is None:
            raise WKTInvalid(
                f'Invalid wkt data. Please, check is the data "{self._data}" is in wkt pattern.'
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

    @typechecked
    def geometries(self, nmax: int = None) -> Generator[GeometryWKT, None, None]:
        ds = self.datasource()
        lyr = ds.GetLayer(0)
        if lyr.GetFeatureCount() == 0:
            yield 'GEOMETRY_EMPTY'

        feat = lyr.GetFeature(0)
        geom = feat.geometry()

        if self._is_geometry_collection(geom):
            for i, geom_item in enumerate(geom):
                yield GeometryWKT(geom_item)

                if i + 1 == nmax:
                    break
        else:
            yield GeometryWKT(geom)

    @typechecked
    def features(self, nmax: int = None):
        raise InvalidOperationForThisDataType('This Data type not has features.')

    @typechecked
    def feature_collection(self, nmax: int = None):
        raise InvalidOperationForThisDataType('This Data type not has feature collection.')

    @typechecked
    def geometry_collection(self, nmax: int = None) -> Union[GeometryCollectionWKT, str]:
        out_wkt = reduce(
            lambda x, y: x + ',' + y, self.geometries(nmax)
        )
        if out_wkt == 'GEOMETRY_EMPTY':
            return 'GEOMETRY_EMPTY'

        if out_wkt.startswith(GEOMETRYCOLLECTION_PREFIX):
            return out_wkt
        else:
            if self._as_geometry_collection:
                return GeometryCollectionWKT(out_wkt)
            else:
                return out_wkt

    #def write(self, ds: DataSource, out_path: str) -> str:
    #    self._validate_basedir(out_path)
    #    return self._write_by_collection(ds, out_path)
