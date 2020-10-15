#!-*-coding:utf-8-*-

import json
from osgeo.ogr import Feature
from typeguard import typechecked


class FeatureGeojson(str):

    @typechecked
    def __new__(cls, feature: Feature):
        content = json.dumps(
            json.loads(feature.ExportToJson()), ensure_ascii=False
        )
        return str.__new__(cls, content)