#!-*-coding:utf-8-*-

from abc import abstractmethod
from osgeo.ogr import DataSource
from typing import Generator
from vectorio.vector.interfaces.ivector import IVector


class IVectorData(IVector):

    @abstractmethod
    def datasource(self, input_data: str) -> DataSource:
        pass

    @abstractmethod
    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def collection(self, datasource: DataSource) -> str:
        pass

    @abstractmethod
    def write(self, ds: DataSource, out_path: str) -> str:
        pass

    def _write_by_collection(self, ds: DataSource, out_path: str) -> str:
        with open(out_path, 'w') as f:
            f.write(self.collection(ds))
        return out_path
