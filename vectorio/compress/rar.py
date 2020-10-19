#!-*-coding:utf-8-*-

import os
import tempfile
from vectorio.compress.icompress_engine import ICompressEngine
from typeguard import typechecked
from rarfile import RarFile


class Rar(ICompressEngine):

    @typechecked
    def decompress(self, fpath: str) -> str:
        tmpdir = tempfile.mkdtemp()
        with RarFile(fpath) as rf:
            rf.extract(tmpdir)
        return tmpdir

    @typechecked
    def compress(self, fpath: str, files: list) -> str:
        str_files = '{} ' * len(files)
        command = f'rar a {fpath} ' + str_files.format(*files) + ' > /dev/null'
        os.system(command)
        return fpath
