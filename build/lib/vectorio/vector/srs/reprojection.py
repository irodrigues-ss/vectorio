#!-*-coding:utf-8-*-

from typing import Generator
from osgeo.ogr import DataSource
from osgeo import ogr, osr
from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector._src.gdal_aux.ds_reprojected import (
    DataSourceReprojected
)


class VectorReprojected(IVectorData):

    _vector = None
    _in_srid = None
    _out_srid = None

    def __init__(
        self, vector: IVectorData, in_srid: int=None, out_srid: int=None
    ):
        self._vector = vector
        self._in_srid = in_srid
        self._out_srid = out_srid

    def datasource(self, input_data: str) -> DataSource:
        return DataSourceReprojected(
            self._vector.datasource(input_data),
            self._in_srid, self._out_srid
        ).ref()

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return self._vector.items(datasource)

    def collection(self, datasource: DataSource) -> str:
        return self._vector.collection(datasource)

    def srid(self, fpath: str) -> int:
        return self._vector.srid(fpath)

    def write(self, ds: DataSource, out_path: str) -> str:
        return self._vector.write(ds, out_path)
