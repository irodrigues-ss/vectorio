#!-*-coding:utf-8-*-

from vectorio.vector.composite.interfaces.ivector_composite import (
    IVectorComposite
)
from vectorio.vector.interfaces.ivector import IVector
from osgeo.ogr import DataSource
from typing import Generator


class VectorComposite(IVectorComposite):

    def __init__(self, input_vector: IVector, output_vector: IVector):
        self._input_vector = input_vector
        self._output_vector = output_vector

    def items(self, input_data: str) -> Generator[str, None, None]:
        return self._output_vector.items(
            self._input_vector.datasource(input_data)
        )

    def collection(self, input_data: str) -> str:
        return self._output_vector.collection(
            self._input_vector.datasource(input_data)
        )

    def write(self, input_data: str, out_path: str) -> str:
        return self._output_vector.write(
            self._input_vector.datasource(input_data), out_path
        )
