#!-*-coding:utf-8-*-

from uuid import uuid4
from osgeo.ogr import DataSource


class GDALClonedLayer:

    _ds = None
    _another_layer = None

    def __init__(self, ds: DataSource, another_layer):
        self._ds = ds
        self._another_layer = another_layer

    def ref(self):
        another_layer_defn = self._another_layer.GetLayerDefn()
        out_lyr = self._ds.CreateLayer(
            str(uuid4()), self._another_layer.GetSpatialRef(),
            geom_type=self._another_layer.GetGeomType()
        )
        for i in range(another_layer_defn.GetFieldCount()):
            out_lyr.CreateField(another_layer_defn.GetFieldDefn(i))
        return out_lyr
