#!-*-coding:utf-8-*-

from functools import reduce


class FeatureCollectionConcatenated(str):

    def __new__(cls, *args, **kwargs):
        features_gen = args[0]
        concat_features_lbd = lambda x, y: str(x) + ',' + str(y)
        features_str = reduce(concat_features_lbd, features_gen)
        return '{"type": "FeatureCollection","features": [' + features_str + ']}'