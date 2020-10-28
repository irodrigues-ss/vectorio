#!-*-coding:utf-8-*-

from vectorio.vector.composite.interfaces.ivector_composite import (
    IVectorComposite
)
from vectorio.vector.interfaces.ivectorio import IVectorIO
from osgeo.ogr import DataSource
from typing import Generator
from typing import Optional
from typeguard import typechecked


class VectorComposite:

    @typechecked
    def __init__(self, input_vector: IVectorIO, output_vector: IVectorIO):
        self._input_vector = input_vector
        self._output_vector = output_vector

    @typechecked
    def features(self, nmax: Optional[int] = None) -> Generator[str, None, None]:
        return self._output_vector.features(
            nmax, self._input_vector.datasource()
        )

    @typechecked
    def geometries(self, nmax: Optional[int] = None) -> Generator[str, None, None]:
        return self._output_vector.geometries(
            nmax, self._input_vector.datasource()
        )

    @typechecked
    def feature_collection(self, nmax: Optional[int] = None) -> str:
        return self._output_vector.feature_collection(
            nmax, self._input_vector.datasource()
        )

    @typechecked
    def geometry_collection(self, nmax: Optional[int] = None) -> str:
        return self._output_vector.geometry_collection(
            nmax, self._input_vector.datasource()
        )

    @typechecked
    def write(self, out_path: str) -> str:
        return self._output_vector.write(
            out_path, self._input_vector.datasource()
        )
