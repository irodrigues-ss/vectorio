#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod


class ICompressEngine(ABC):

    @abstractmethod
    def compress(self, fpath: str, files: list) -> str:
        pass

    @abstractmethod
    def decompress(self, fpath: str) -> str:
        pass
