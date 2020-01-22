#!-*-coding:utf-8-*-

import os
import shutil
import tempfile
from typing import Generator
from osgeo.ogr import DataSource
from vectorio.vector.interfaces.ivector_file import IVectorFile
from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
from rarfile import RarFile


class ShapefileAsRar(IVectorFile):

    _shapefile = None

    def __init__(self, shapefile: IVectorFile):
        self._shapefile = shapefile

    def _extraction_dir(self, fpath: str) -> str:
        tmpdir = tempfile.mkdtemp()
        with RarFile(fpath) as rf:
            rf.extract(tmpdir)
        return tmpdir

    def _compress_files(self, fpath: str, files: list) -> str:
        str_files = '{} ' * len(files)
        command = f'rar a {fpath} ' + str_files.format(*files) + ' > /dev/null'
        os.system(command)
        return fpath

    def datasource(self, fpath: str) -> DataSource:
        dir_with_files = self._extraction_dir(fpath)
        files_required = FileRequiredByExtension(
            dir_with_files, ['shp', 'dbf', 'shx', 'prj']
        )
        ds = self._shapefile.datasource(files_required.files()['shp'])
        shutil.rmtree(dir_with_files)
        return ds

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return self._shapefile.items(datasource)

    def collection(self, datasource: DataSource):
        return self._shapefile.collection(datasource)

    def write(self, ds: DataSource, out_path: str) -> str:
        assert out_path.endswith('.rar'), 'Output file have has .rar extension.'
        out_shp = self._shapefile.write(ds, out_path.replace('.rar', '.shp'))

        files = [
            out_shp,
            out_shp.replace('.shp', '.dbf'),
            out_shp.replace('.shp', '.prj'),
            out_shp.replace('.shp', '.shx')
        ]
        out_rar = self._compress_files(out_path, files)
        for f in files:
            os.remove(f)
        return out_rar
