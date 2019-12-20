#!-*-coding:utf-8-*-

from osgeo.ogr import DataSource
from typing import Generator
from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.interfaces.ivector_file import IVectorFile


class GeoFile(IVectorFile):

    _vector = None

    def __init__(self, vector: IVectorData):
        self._vector = vector

    def datasource(self, fpath: str) -> DataSource:
        with open(fpath) as geof:
            return self._vector.datasource(geof.read())

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return self._vector.items(datasource)

    def collection(self, datasource: DataSource) -> str:
        return self._vector.collection(datasource)

    def write(self, ds: DataSource, out_path: str) -> str:
        self._vector.write(ds, out_path)
