
from uuid import uuid4
from typing import Generator
from functools import reduce
from osgeo.ogr import Geometry, DataSource, Feature
from typeguard import typechecked
from typing import Union
from vectorio.config import GEOMETRYCOLLECTION_PREFIX, GEOM_COLLECTION_LEN
from vectorio.vector.output.wkt.geometry import GeometryWKT
from vectorio.vector.output.wkt.geometry_collection import GeometryCollectionWKT


class WKTGeometry:

    def __init__(self, ds: DataSource, as_geometry_collection: bool = True):
        self._ds = ds
        self._as_geometry_collection = as_geometry_collection

    # @typechecked
    # def _is_geometry_collection(self, geom: Geometry) -> bool:
    #    return geom.ExportToWkt()[:GEOM_COLLECTION_LEN].startswith(GEOMETRYCOLLECTION_PREFIX)

    @typechecked
    def geometries(self, nmax: int = None) -> Generator[GeometryWKT, None, None]:
        ds = self._ds
        lyr = ds.GetLayer(0)
        if lyr.GetFeatureCount() == 0:
            yield GeometryWKT() # GeometryEmpty

        for feat in lyr:
            geom = feat.geometry()
            yield GeometryWKT(geom)

        lyr.ResetReading()

    @typechecked
    def collection(self, nmax: int = None) -> Union[GeometryCollectionWKT, str]:
        out_wkt = reduce(
            lambda x, y: x + ',' + y, self.geometries(nmax)
        )
        if out_wkt == 'GEOMETRY_EMPTY':
            return 'GEOMETRY_EMPTY'

        if out_wkt.startswith(GEOMETRYCOLLECTION_PREFIX):
            return out_wkt
        else:
            if self._as_geometry_collection:
                return GeometryCollectionWKT(out_wkt)
            else:
                return out_wkt