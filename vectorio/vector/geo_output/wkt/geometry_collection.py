#!-*-coding:utf-8-*-
from typeguard import typechecked
from vectorio.config import GEOMETRYCOLLECTION_PREFIX


class GeometryCollectionWKT(str):

    @typechecked
    def __new__(cls, wkt_str: str):
        return str.__new__(cls, f'{GEOMETRYCOLLECTION_PREFIX} ({wkt_str})')