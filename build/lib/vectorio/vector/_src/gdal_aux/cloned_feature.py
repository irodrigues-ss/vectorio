#!-*-coding:utf-8-*-

from osgeo import ogr


class GDALClonedFeature:

    _gdal_feature_ref = None
    _geom = None
    _layer_dfn = None
    _another_feature = None

    def __init__(self, layer_dfn, geom, another_feature):
        self._geom = geom
        self._layer_dfn = layer_dfn
        self._another_feature = another_feature

    def ref(self):
        gdal_feature_ref = ogr.Feature(self._layer_dfn)
        gdal_feature_ref.SetGeometry(self._geom)

        for i in range(self._layer_dfn.GetFieldCount()):
            field_name = self._layer_dfn.GetFieldDefn(i).GetNameRef()
            field_value = self._another_feature.GetField(i)
            gdal_feature_ref.SetField(field_name, field_value)

        return gdal_feature_ref
