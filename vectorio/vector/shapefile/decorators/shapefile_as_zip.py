#!-*-coding:utf-8-*-

import os
import shutil
from typing import Generator
from osgeo.ogr import DataSource

from vectorio.vector.geo_output.geojson.feature import FeatureGeojson
from vectorio.vector.geo_output.geojson.feature_collection import FeatureCollectionGeojson
from vectorio.vector.geo_output.geojson.geometry import GeometryGeojson
from vectorio.vector.geo_output.geojson.geometry_collection import GeometryCollectionGeojson
from vectorio.vector.interfaces.ivector_file import IVectorFile
from zipfile import ZipFile
from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
import tempfile

from typeguard import typechecked
from typing import Optional


class ShapefileAsZip:

    _shapefile = None

    def __init__(self, shapefile: IVectorFile):
        self._shapefile = shapefile

    @typechecked
    def _extraction_dir(self, fpath: str) -> str:
        tmpdir = tempfile.mkdtemp()
        with ZipFile(fpath) as zipf:
            zipf.extractall(tmpdir)
        return tmpdir

    def _compress_files(self, fpath: str, files: list) -> str:
        with ZipFile(fpath, 'w') as zipf:
            for f in files:
                zipf.write(f)
        return fpath

    @typechecked
    def datasource(self) -> DataSource:
        dir_with_files = self._extraction_dir(self._shapefile.path())
        files_required = FileRequiredByExtension(
            dir_with_files, ['shp', 'dbf', 'shx', 'prj']
        )
        ds = self._shapefile.datasource(files_required.files()['shp'])
        shutil.rmtree(dir_with_files)
        return ds

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

    def write(self, ds: DataSource, out_path: str) -> str:
        assert out_path.endswith('.zip'), 'Output file have has .zip extension.'
        out_shp = self._shapefile.write(ds, out_path.replace('.zip', '.shp'))
        files = [
            out_shp,
            out_shp.replace('.shp', '.dbf'),
            out_shp.replace('.shp', '.prj'),
            out_shp.replace('.shp', '.shx')
        ]
        out_zip = self._compress_files(out_path, files)
        for f in files:
            os.remove(f)
        return out_zip
