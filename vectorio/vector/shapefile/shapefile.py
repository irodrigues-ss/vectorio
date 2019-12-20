#!-*-coding:utf-8-*-

# import fiona
import os
import json
from functools import reduce
from typing import Generator
from osgeo import ogr, osr
from osgeo.ogr import DataSource, Feature
from vectorio.vector.interfaces.ivector_file import IVectorFile
from vectorio.vector.shapefile.decorators.shapefile_extracted import (
    ShapefileExtracted
)
from vectorio.vector._src.generators.generator_geojson import GeneratorGeojson
from vectorio.vector._src.generators.feature_collection_concatenated import (
    FeatureCollectionConcatenated
)
from vectorio.vector._src.generators.generator_with_feature_processor import (
    GeneratorWithFeatureProcessor
)
from vectorio.vector.exceptions import (
    ShapefileInvalid, ShapefileIsEmpty,
    ImpossibleCreateShapefileFromGeometryCollection
)
from vectorio.vector._src.cpfs.factory import CompressedFilesFactory
from vectorio.vector.shapefile.file_required_by_extension import (
    FileRequiredByExtension
)
from uuid import uuid4


os.environ['SHAPE_ENCODING'] = "UTF-8"


@ShapefileExtracted
class Shapefile(IVectorFile):

    _driver = None

    def __init__(self):
        self._driver = ogr.GetDriverByName('ESRI Shapefile')

    def _has_data(self, ds: DataSource):
        lyr = ds.GetLayer()
        if lyr.GetFeature(0) is None:
            raise ShapefileIsEmpty(
                "Shapefile is empty. Please, check if your shapefile has data."
            )

    def datasource(self, fpath: str) -> DataSource:
        ds = self._driver.Open(fpath)
        if ds is None:
            raise ShapefileInvalid(
                'Shapefile invalid. Please, check if your shapefile is correct.'
            )
        self._has_data(ds)
        return ds

    def items(self, datasource: DataSource) -> Generator[str, None, None]:
        return GeneratorGeojson(
            GeneratorWithFeatureProcessor(datasource)
        ).features()

    def collection(self, datasource: DataSource) -> str:
        return FeatureCollectionConcatenated(self.items(datasource))

    def write(self, ds: DataSource, out_path: str,) -> str:
        assert out_path.endswith('.shp'), 'Output file have has .shp extension.'
        lyr = ds.GetLayer()
        feat = lyr.GetFeature(0)

        if feat.geometry().GetGeometryName() == 'GEOMETRYCOLLECTION':
            raise ImpossibleCreateShapefileFromGeometryCollection(
                'Impossible create shapefile from a geometry collection.'
                ' Please, convert the geometry collection for feature '
                'collection with same geometry type.'
            )

        ds_out = self._driver.CreateDataSource(out_path)
        ds_out.CopyLayer(ds.GetLayer(), str(uuid4()))
        ds_out.Destroy()
        return out_path
