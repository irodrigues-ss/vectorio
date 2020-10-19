#!-*-coding:utf-8-*-

from vectorio.vector.composite.interfaces.ivector_composite import (
    IVectorComposite
)
from vectorio.vector.interfaces.ivector import IVector
from osgeo.ogr import DataSource
from typing import Generator
from typing import Optional


class VectorComposite:

    def __init__(self, input_vector: IVector, output_vector: IVector):
        self._input_vector = input_vector
        self._output_vector = output_vector

    def features(self, nmax: Optional[int] = None) -> Generator[str, None, None]:
        return self._output_vector.features(
            nmax, self._input_vector.datasource()
        )

    def geometries(self, nmax: Optional[int] = None) -> Generator[str, None, None]:
        return self._output_vector.geometries(
            nmax, self._input_vector.datasource()
        )

    def feature_collection(self, nmax: Optional[int] = None) -> str:
        return self._output_vector.feature_collection(
            nmax, self._input_vector.datasource()
        )

    def geometry_collection(self, nmax: Optional[int] = None) -> str:
        return self._output_vector.geometry_collection(
            nmax, self._input_vector.datasource()
        )

    def write(self, out_path: str) -> str:
        return self._output_vector.write(
            out_path, self._input_vector.datasource()
        )
