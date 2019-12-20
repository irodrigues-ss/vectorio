#!-*-coding:utf-8-*-

import os
import tempfile
import shutil

from vectorio.vector.interfaces.ivector_file import IVectorFile
from osgeo.ogr import DataSource
from typing import Generator
from zipfile import ZipFile
from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
from vectorio.vector._src.cpfs.factory import CompressedFilesFactory
from vectorio.vector._src.gdal_aux.cloned_ds import (
    GDALClonedDataSource
)
from contextlib import contextmanager


class ShapefileExtracted(IVectorFile):

    _vector_obj = None
    _vector_cls = None

    def __init__(self, clss):
        self._vector_cls = clss

    def __call__(self, *args, **kwargs):
        self._vector_obj = self._vector_cls(*args, **kwargs)
        return self

    def datasource(self, fpath: str) -> DataSource:
        """
        clonning datasource for load all objects (spatial reference) data for
        memory
        """
        if fpath.endswith('.shp'):
            return GDALClonedDataSource(
                self._vector_obj.datasource(fpath)
            ).ref()
        else:
            compressed_files = CompressedFilesFactory(fpath).create()
            files_required = FileRequiredByExtension(
                compressed_files.extraction_dir(), ['shp', 'dbf', 'shx', 'prj']
            )
            ds = self._vector_obj.datasource(files_required.files()['shp'])
            out_ds = GDALClonedDataSource(ds).ref()
            compressed_files.remove_extraction_dir()
            return out_ds

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return self._vector_obj.items(datasource)

    def collection(self, datasource: DataSource):
        return self._vector_obj.collection(datasource)

    # def srid(self, fpath: str) -> int:
    #     return self._vector_obj.srid(fpath)

    def write(self, ds: DataSource, out_path: str) -> str:
        return self._vector_obj.write(ds, out_path)
