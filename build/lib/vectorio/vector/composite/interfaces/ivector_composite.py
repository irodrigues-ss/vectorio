# -*-coding:utf-8-*-

from abc import ABC, abstractmethod
from typing import Generator
from osgeo.ogr import DataSource


class IVectorComposite(ABC):

    @abstractmethod
    def items(self, input_data: str) -> Generator[str, None, None]:
        """Docs"""
        pass

    @abstractmethod
    def collection(self, input_data: str) -> str:
        """ Docs """
        pass

    @abstractmethod
    def write(self, input_data: str, out_path: str) -> str:
        """ Docs """
        pass
