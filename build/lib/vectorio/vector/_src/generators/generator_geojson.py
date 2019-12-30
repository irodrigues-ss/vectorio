#!-*-coding:utf-8-*-

import json
from typing import Generator
from osgeo.ogr import DataSource
from vectorio.vector._src.generators.generator_with_feature_processor import (
    GeneratorWithFeatureProcessor
)


class GeneratorGeojson:

    _gen = None

    def __init__(self, gen: GeneratorWithFeatureProcessor):
        self._gen = gen

    def features(self) -> Generator[str, None, None]:
        feature_processor = lambda feature: json.dumps(json.loads(feature.ExportToJson()), ensure_ascii=False) # removing ascii codec
        next(self._gen)
        self._gen.send(feature_processor)
        return self._gen
