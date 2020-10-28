#!-*-coding:utf-8-*-

import os
import shutil
from typing import Generator
from osgeo.ogr import DataSource

from vectorio.compress.icompress_engine import ICompressEngine
from vectorio.compress.zip_file import Zip
from vectorio.vector.output.geojson.feature import FeatureGeojson
from vectorio.vector.output.geojson.feature_collection import FeatureCollectionGeojson
from vectorio.vector.output.geojson.geometry import GeometryGeojson
from vectorio.vector.output.geojson.geometry_collection import GeometryCollectionGeojson
from vectorio.vector.interfaces.ivectorio import IVectorIO

from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
from typeguard import typechecked
from typing import Optional, Union
from vectorio.config import NoneType


class ShapefileCompressed(IVectorIO):

    _shapefile = None
    _compress_engine: ICompressEngine

    @typechecked
    def __init__(self, shapefile: object, compress_engine: ICompressEngine = Zip()):
        self._shapefile = shapefile
        self._compress_engine = compress_engine

    @typechecked
    def datasource(self) -> DataSource:
        dir_with_files = self._compress_engine.decompress(self._shapefile.source())
        files_required = FileRequiredByExtension(
            dir_with_files, ['shp', 'dbf', 'shx', 'prj']
        )
        ds = self._shapefile.datasource(files_required.files()['shp'])
        shutil.rmtree(dir_with_files)
        return ds

    @typechecked
    def source(self) -> Union[str, NoneType]:
        return self._shapefile.source()

    @typechecked
    def features(self, nmax: Optional[int] = None, ds: DataSource = None) -> Generator[FeatureGeojson, None, None]:
        if ds is None:
            return self._shapefile.features(nmax, self.datasource())
        return self._shapefile.features(nmax, ds)

    @typechecked
    def geometries(self, nmax: Optional[int] = None, ds: DataSource = None) -> Generator[GeometryGeojson, None, None]:
        if ds is None:
            return self._shapefile.geometries(nmax, self.datasource())
        return self._shapefile.geometries(nmax, ds)

    @typechecked
    def feature_collection(self, nmax: Optional[int] = None, ds: DataSource = None) -> FeatureCollectionGeojson:
        if ds is None:
            return self._shapefile.feature_collection(nmax, self.datasource())
        return self._shapefile.feature_collection(nmax, ds)

    @typechecked
    def geometry_collection(self, nmax: Optional[int] = None, ds: DataSource = None) -> GeometryCollectionGeojson:
        if ds is None:
            return self._shapefile.geometry_collection(nmax, self.datasource())
        return self._shapefile.geometry_collection(nmax, ds)

    @typechecked
    def _write(self, ds: DataSource, out_path: str) -> str:
        assert out_path.endswith('.zip'), 'Output file have has .zip extension.'
        out_shp = self._shapefile.write(out_path.replace('.zip', '.shp'), ds=ds)
        files = [
            out_shp,
            out_shp.replace('.shp', '.dbf'),
            out_shp.replace('.shp', '.prj'),
            out_shp.replace('.shp', '.shx')
        ]
        out_zip = self._compress_engine.compress(out_path, files)
        for f in files:
            os.remove(f)
        return out_zip

    @typechecked
    def write(self, out_path: str, ds: DataSource = None) -> str:
        if ds is None:
            return self._write(self.datasource(), out_path)
        return self._write(ds, out_path)
