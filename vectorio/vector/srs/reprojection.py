#!-*-coding:utf-8-*-

from typing import Generator
from osgeo.ogr import DataSource
from osgeo import ogr, osr
from vectorio.vector.interfaces.ivectorio import IVectorIO
from vectorio.vector import DataSourceReprojected
from typing import Optional


class VectorReprojected(IVectorIO):

    _vector = None
    _in_srid = None
    _out_srid = None

    def __init__(
        self, vector: IVectorIO, in_srid: int=None, out_srid: int=None
    ):
        self._vector = vector
        self._in_srid = in_srid
        self._out_srid = out_srid

    def datasource(self, source: str = None) -> DataSource:
        if source is None:
            ds = self._vector.datasource()
        else:
            ds = self._vector.datasource(source)
        return DataSourceReprojected(ds, self._in_srid, self._out_srid).ref()

    def source(self):
        return self._vector.source()

    def geometries(self, nmax: int = None, ds: DataSource = None) -> Generator[str, None, None]:
        if ds is None:
            return self._vector.geometries(nmax, self.datasource())
        return self._vector.geometries(nmax, ds)

    def features(self, nmax: int = None, ds: DataSource = None) -> Generator[str, None, None]:
        if ds is None:
            return self._vector.features(nmax, self.datasource())
        return self._vector.features(nmax, ds)

    def feature_collection(self, nmax: Optional[int] = None, ds: Optional[DataSource] = None):
        if ds is None:
            return self._vector.feature_collection(nmax, self.datasource())
        return self._vector.feature_collection(nmax, ds)

    def geometry_collection(self, nmax: Optional[int] = None, ds: Optional[DataSource] = None):
        if ds is None:
            return self._vector.geometry_collection(nmax, self.datasource())
        return self._vector.geometry_collection(nmax, ds)

    def write(self, out_path: str, ds: DataSource = None) -> str:
        if ds is None:
            return self._vector.write(out_path, ds=self.datasource())
        return self._vector.write(out_path, ds=ds)
