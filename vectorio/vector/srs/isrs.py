#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod
from osgeo.osr import SpatialReference
from osgeo.ogr import Layer
from vectorio.exceptions import DataSourceWithoutSpatialRef


class ISRS(ABC):

    def _srs_from_layer(self, lyr: Layer, ds_name: str) -> SpatialReference:
        in_spatial_ref = lyr.GetSpatialRef()

        if in_spatial_ref is None:
            raise DataSourceWithoutSpatialRef(
                f'The datasource {ds_name} not have spatial'
                ' reference. Plese, use the input SRID.'
            )
        return in_spatial_ref

    @abstractmethod
    def input_srs(self) -> SpatialReference:
        pass

    @abstractmethod
    def output_srs(self) -> SpatialReference:
        pass
