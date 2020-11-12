#!-*-coding:utf-8-*-

from uuid import uuid4
from typing import Generator, Optional
from osgeo import ogr, osr
from osgeo.ogr import Geometry, DataSource, Feature

from vectorio.vector.output.wkt.geometry import GeometryWKT
from vectorio.vector.output.wkt.geometry_collection import GeometryCollectionWKT
from vectorio.vector.interfaces.ivectorio import IVectorIO
from vectorio.vector.exceptions import WKTInvalid, InvalidOperationForThisDataType
from vectorio.vector.wkt.geom_type_factory import GeometryTypeFactory
from vectorio.config import GDAL_DRIVERS_NAME, NoneType
from typeguard import typechecked
from typing import Union
from vectorio.vector.wkt.wkt_geom_collec import WKTGeometry


class WKT(IVectorIO):

    _gt_factory: GeometryTypeFactory
    _initial_srid: int
    _as_geometry_collection: bool
    _data: str

    def __init__(self, data: str = None, as_geometry_collection=True, srid=4326):
        self._gt_factory = GeometryTypeFactory()
        self._data = data
        self._initial_srid = srid
        self._as_geometry_collection = as_geometry_collection

    def _srs(self):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self._initial_srid)
        return srs

    @typechecked
    def source(self) -> Union[str, NoneType]:
        return self._data

    @typechecked
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
    def geometries(
            self, nmax: int = None, ds: Optional[Union[DataSource, NoneType]] = None
    ) -> Generator[str, None, None]:
        """
        Obs: the "nmax" actually not has effect in WKT data, this parameter exists for keep the interface.
        """
        wkt_geom = WKTGeometry(ds, self._as_geometry_collection)
        if ds is None:
            wkt_geom = WKTGeometry(self.datasource(), self._as_geometry_collection)
        return wkt_geom.geometries()

    @typechecked
    def features(
        self,  nmax: int = None, ds: Optional[Union[DataSource, NoneType]] = None
    ):
        raise InvalidOperationForThisDataType('This Data type not has features.')

    @typechecked
    def feature_collection(
        self, ds: Optional[Union[DataSource, NoneType]] = None
    ):
        raise InvalidOperationForThisDataType('This Data type not has feature collection.')

    @typechecked
    def geometry_collection(
        self, nmax: int = None, ds: Optional[Union[DataSource, NoneType]] = None
    ) -> Union[GeometryCollectionWKT, str]:
        """
        Obs: the "nmax" actually not has effect in WKT data, this parameter exists for keep the interface.
        """
        wkt_geom = WKTGeometry(ds, self._as_geometry_collection)
        if ds is None:
            wkt_geom = WKTGeometry(self.datasource(), self._as_geometry_collection)
        return wkt_geom.collection()

    @typechecked
    def _write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        with open(out_path, 'w') as f:
            f.write(self.geometry_collection(ds=ds))
        return out_path

    @typechecked
    def write(self, out_path: str, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        if ds is None:
            return self._write(self.datasource(), out_path)
        return self._write(ds, out_path)
