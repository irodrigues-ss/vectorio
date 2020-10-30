#!-*-coding:utf-8-*-

import tempfile
from zipfile import ZipFile
from vectorio.compress.icompress_engine import ICompressEngine
from typeguard import typechecked


class Zip(ICompressEngine):

    @typechecked
    def decompress(self, fpath: str) -> str:
        tmpdir = tempfile.mkdtemp()
        with ZipFile(fpath) as zipf:
            zipf.extractall(tmpdir)
        return tmpdir

    @typechecked
    def compress(self, fpath: str, files: list) -> str:
        with ZipFile(fpath, 'w') as zipf:
            for f in files:
                zipf.write(f)
        return fpath
