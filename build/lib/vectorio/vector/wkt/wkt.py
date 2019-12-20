#!-*-coding:utf-8-*-

from uuid import uuid4
from typing import Generator
from functools import reduce

from osgeo import ogr, osr
from osgeo.ogr import Geometry, DataSource, Feature

from vectorio.vector.interfaces.ivector_data import IVectorData
from vectorio.vector.exceptions import WKTInvalid
from vectorio.vector.wkt.geom_type_factory import GeometryTypeFactory
from vectorio.vector._src.generators.generator_with_feature_processor import (
    GeneratorWithFeatureProcessor
)

GEOMETRYCOLLECTION_PREFIX = 'GEOMETRYCOLLECTION'


class WKT(IVectorData):

    _gt_factory = None
    _inp_ds = None
    _out_ds = None
    _initial_srid = 4326

    def __init__(self):
        drv = ogr.GetDriverByName('MEMORY')
        self._inp_ds = drv.CreateDataSource('inputData')
        self._out_ds = drv.CreateDataSource('outputData')
        self._gt_factory = GeometryTypeFactory()

    def _srs(self):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(self._initial_srid)
        return srs

    def datasource(self, input_data: str) -> DataSource:
        geom = None
        if not bool(input_data):
            raise WKTInvalid(
                'Invalid wkt data. Please, check if data is a wkt valid.'
            )

        geom = ogr.CreateGeometryFromWkt(input_data)

        if geom is None:
            raise WKTInvalid(
                f'Invalid wkt data. Please, check is the data "{input_data}" is in wkt pattern.'
            )
        l1 = self._out_ds.CreateLayer(
            str(uuid4()), self._srs(),
            self._gt_factory.get_type(geom.GetGeometryName())
        )
        feat = ogr.Feature(l1.GetLayerDefn())
        feat.SetGeometry(geom)
        # this change on this layer "l1" will be reflected on "_out_ds"
        l1.SetFeature(feat)
        return self._out_ds

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        gen = GeneratorWithFeatureProcessor(datasource)
        feature_processor = lambda feature: feature.geometry().ExportToWkt()
        next(gen)
        gen.send(feature_processor)
        return gen

    def collection(self, datasource: DataSource) -> str:
        concat_geometries_lbd = lambda x, y: str(x) + ',' + str(y)
        geometries_str = reduce(
            concat_geometries_lbd, self.items(datasource)
        )
        if geometries_str.startswith(GEOMETRYCOLLECTION_PREFIX):
            return geometries_str
        return f'{GEOMETRYCOLLECTION_PREFIX} ({geometries_str})'

    def write(self, ds: DataSource, out_path: str) -> str:
        self._validate_basedir(out_path)
        return self._write_by_collection(ds, out_path)
