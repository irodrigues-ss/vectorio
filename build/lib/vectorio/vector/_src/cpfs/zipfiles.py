#!-*-coding:utf-8-*-

import os
import tempfile
from zipfile import ZipFile
from vectorio.vector._src.cpfs.interfaces.icompressed_files import (
    ICompressedFiles
)


class Zipfiles(ICompressedFiles):

    _fpath = ''

    def __init__(self, fpath: str):
        self._fpath = fpath
        self._tmpdir = tempfile.mkdtemp()

    def extraction_dir(self) -> str:
        with ZipFile(self._fpath) as zipf:
            zipf.extractall(self._tmpdir)
        return self._tmpdir
