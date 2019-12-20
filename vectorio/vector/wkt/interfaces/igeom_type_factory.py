#!-*-coding:utf-8-*-

from abc import ABC, abstractmethod


class IGeometryTypeFactory(ABC):

    def get_type(self, geom_type: str) -> int:
        pass
