#!-*-coding:utf-8-*-

import json
from osgeo.ogr import Feature
from vectorio.config import NoneType
from typing import Union


class FeatureGeojson(str):

    def __new__(cls, feature: Union[Feature, NoneType]):
        if feature is None:
            return None

        content = json.dumps(
            json.loads(feature.ExportToJson()), ensure_ascii=False
        )
        return str.__new__(cls, content)