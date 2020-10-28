#!-*-coding:utf-8-*-
import os
from abc import ABC, abstractmethod
from osgeo.ogr import DataSource
from vectorio.vector.exceptions import DirectoryDoesNotExists
from vectorio.vector.metrics.vertices import Vertices
from typing import Any, Optional, Generator, Union
from vectorio.config import NoneType
from typeguard import typechecked


class IVectorIO(ABC):

    @abstractmethod
    def datasource(self) -> DataSource:
        pass

    @abstractmethod
    def source(self) -> Any:
        pass

    @abstractmethod
    def features(self, nmax: Optional[int] = None, ds: Optional[Union[DataSource, NoneType]] = None) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def geometries(self, nmax: Optional[int] = None, ds: Optional[Union[DataSource, NoneType]] = None) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def feature_collection(self, nmax: Optional[int] = None, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        pass

    @abstractmethod
    def geometry_collection(self, nmax: Optional[int] = None, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        pass

    @abstractmethod
    def write(self, out_path: str, ds: Optional[Union[DataSource, NoneType]] = None) -> str:
        pass

    @typechecked
    def vertices_by_feature(self, ds: Optional[Union[DataSource, NoneType]] = None):
        if ds is None:
            ds = self.datasource()

        vertices = Vertices() # Should renamed to "Vertice"
        lyr = ds.GetLayer(0)
        vertices_count = {}
        for feat_idx in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(feat_idx)
            geom = feat.geometry()

            if geom is None:
                feat_id = f'Feature_{feat_idx}_NULL'
                vertices_count[feat_id] = [0]
            else:
                if geom.GetGeometryName() == 'GEOMETRYCOLLECTION':
                    for i, inner_geom in enumerate(geom):

                        if inner_geom is None:
                            feat_id = f'Feature_{feat_idx}_Geom_{i}_NULL'
                            vertices_count[feat_id] = [0]
                        else:
                            feat_id = f'Feature_{feat_idx}_Geom_{i}_{inner_geom.GetGeometryName()}'
                            vertices_count[feat_id] = vertices.tell(inner_geom)
                else:
                    feat_id = f'Feature_{feat_idx}_{geom.GetGeometryName()}'
                    vertices_count[feat_id] = vertices.tell(geom)

        return vertices_count

    @typechecked
    def _validate_basedir(self, out_path: str):
        dirname = os.path.dirname(out_path)
        if dirname != '':
            if not os.path.exists(dirname):
                raise DirectoryDoesNotExists(
                    f'The directory "{dirname}" does not exists.'
                )
