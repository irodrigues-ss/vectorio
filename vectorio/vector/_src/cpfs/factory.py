#!-*-coding:utf-8-*-

from vectorio.vector._src.cpfs.interfaces.icompressed_files import (
    ICompressedFiles
)
from vectorio.vector._src.cpfs.interfaces.icompressed_files_factory import (
    ICompressedFilesFactory
)
from vectorio.vector._src.cpfs.zipfiles import Zipfiles
from vectorio.vector._src.cpfs.rarfiles import Rarfiles
from vectorio.vector.exceptions import TypeFromFileIsNotSupported


class CompressedFilesFactory(ICompressedFilesFactory):

    _fpath = ''

    def __init__(self, fpath: str):
        self._fpath = fpath

    def create(self) -> ICompressedFiles:
        # When add a new extension support, update also the exceptions message.
        fext = self._fpath.split('.')[-1].lower()
        if fext == 'zip':
            return Zipfiles(self._fpath)
        elif fext == 'rar':
            return Rarfiles(self._fpath)
        else:
            raise TypeFromFileIsNotSupported(
                f'the file {self._fpath} has a extension not supported. '
                'Allowed extensions: ".zip", ".rar".'
            )
