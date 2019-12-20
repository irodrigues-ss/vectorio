#!-*-coding:utf-8-*-

import os
from typing import Generator
from osgeo.ogr import DataSource
from vectorio.vector.interfaces.ivector_file import IVectorFile
from zipfile import ZipFile


class ShapefileAsZip(IVectorFile):

    _shapefile = None

    def __init__(self, shapefile: IVectorFile):
        self._shapefile = shapefile

    def datasource(self, fpath: str) -> DataSource:
        return self._shapefile.datasource(fpath)

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return self._shapefile.items(datasource)

    def collection(self, datasource: DataSource):
        return self._shapefile.collection(datasource)

    def _compress_files(self, fpath: str, files: list) -> str:
        with ZipFile(fpath, 'w') as zipf:
            for f in files:
                zipf.write(f)
        return fpath

    def write(self, ds: DataSource, out_path: str) -> str:
        out_shp = self._shapefile.write(ds, out_path)
        files = [
            out_shp,
            out_shp.replace('.shp', '.dbf'),
            out_shp.replace('.shp', '.prj'),
            out_shp.replace('.shp', '.shx')
        ]
        out_zip = self._compress_files(out_shp.replace('.shp', '.zip'), files)
        for f in files:
            os.remove(f)
        return out_zip
