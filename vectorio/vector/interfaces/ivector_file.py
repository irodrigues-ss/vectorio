#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod
from osgeo.ogr import DataSource
from typing import Generator
from vectorio.vector.interfaces.ivector import IVector


class IVectorFile(IVector):

    @abstractmethod
    def datasource(self, fpath: str) -> DataSource:
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
