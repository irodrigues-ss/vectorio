#!-*-coding:utf-8-*-

import tempfile
from rarfile import RarFile
from vectorio.vector._src.cpfs.interfaces.icompressed_files import (
    ICompressedFiles
)


class Rarfiles(ICompressedFiles):

    _fpath = ''

    def __init__(self, fpath: str):
        self._fpath = fpath
        self._tmpdir = tempfile.mkdtemp()

    def extraction_dir(self) -> str:
        with RarFile(self._fpath) as rf:
            rf.extract(self._tmpdir)
        return self._tmpdir
