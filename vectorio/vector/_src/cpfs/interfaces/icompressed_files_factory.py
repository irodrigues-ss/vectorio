#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod
from vectorio.vector._src.cpfs.interfaces.icompressed_files import (
    ICompressedFiles
)


class ICompressedFilesFactory(ABC):

    @abstractmethod
    def create(self) -> ICompressedFiles:
        pass
