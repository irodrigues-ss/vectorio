#!-*-coding:utf-8-*-

from functools import reduce


class GeometryCollectionGeojson(str):

    def __new__(cls, *args, **kwargs):
        features_gen = args[0]
        concat_features_lbd = lambda x, y: str(x) + ',' + str(y)
        geometries_str = reduce(concat_features_lbd, features_gen)
        return str.__new__(cls, '{"type": "GeometryCollection","geometries": [' + geometries_str + ']}')
