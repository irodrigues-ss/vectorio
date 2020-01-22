#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod


class IFileRequiredByExtension(ABC):

    @abstractmethod
    def files(self) -> dict:
        pass
