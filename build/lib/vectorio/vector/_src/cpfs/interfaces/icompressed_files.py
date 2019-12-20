#!-*-coding:utf-8-*-

import shutil
from abc import ABC, abstractmethod


class ICompressedFiles(ABC):

    _tmpdir = ''

    @abstractmethod
    def extraction_dir(self) -> str:
        pass

    def remove_extraction_dir(self):
        shutil.rmtree(self._tmpdir)
