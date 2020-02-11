#!-*-coding:utf-8-*-
import os
from osgeo import ogr
from osgeo.ogr import DataSource
from vectorio.vector import (
    Shapefile as ShapefileLG, ShapefileAsZip, WKT
)
from vectorio.config import STATIC_DIR
from vectorio.vector.exceptions import (
    ErrorOnIntersection, ExistsManyGeometriesTypes
)


class UTMZone:

    _drv_mem = None
    _world_utm_grid_ds = None

    def __init__(self):
        self._world_utm_grid_ds = ShapefileAsZip(
            ShapefileLG()
        ).datasource(
            os.path.join(STATIC_DIR, 'World_UTM_Grid_HM.zip')
        )
        self._drv_mem = ogr.GetDriverByName('MEMORY')

    def _intersection_ds(self, ds_utm: DataSource, inp_ds: DataSource):
        lyr_utm = ds_utm.GetLayer(0)
        target_lyr = inp_ds.GetLayer(0)
        ds_out = self._drv_mem.CreateDataSource('out_mem_ds')
        lyr_out = ds_out.CreateLayer('out_mem_Lyr')
        intersection = lyr_utm.Intersection(target_lyr, lyr_out)

        if intersection != 0:
            raise ErrorOnIntersection(
                "Error on Intersection. Please, check if your datasource is valid."
            )
        return ds_out

    def zones(self, inp_ds: DataSource) -> set:
        ds = self._intersection_ds(self._world_utm_grid_ds, inp_ds)
        lyr = ds.GetLayer(0)
        result = set()

        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            zone = f'{feat.GetFieldAsInteger("ZONE")}{feat.GetFieldAsString("HEMISPHERE")}'
            result.add(zone)
        return result

    def zone_from_biggest_geom(self, inp_ds: DataSource):
        ds = self._intersection_ds(self._world_utm_grid_ds, inp_ds)
        biggest_part_idx = 0
        indexes_from_feats = []  # all indexes from features
        metrics = []  # area or length of the geometry from feature
        all_geom_type = set()
        lyr = ds.GetLayer(0)

        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            geom_type = feat.geometry().GetGeometryName()
            area_or_length = 0
            all_geom_type.add(geom_type)

            if len(all_geom_type) != 1:
                # validating if the geometries types are from same type
                raise ExistsManyGeometriesTypes(
                    "Many geometries types are not supported."
                )

            if geom_type == 'POLYGON':
                area_or_length = feat.geometry().Area()
            elif geom_type == 'LINESTRING':
                area_or_length = feat.geometry().Length()
            else:
                area_or_length = 0

            indexes_from_feats.append(idx_feat)
            metrics.append(area_or_length)

        # getting index from biggest geometry by feature
        biggest_part_idx = indexes_from_feats[
            metrics.index(  # getting index by value
                max(metrics)  # getting max area or length
            )
        ]
        feat = lyr.GetFeature(biggest_part_idx)
        zone = f'{feat.GetFieldAsInteger("ZONE")}{feat.GetFieldAsString("HEMISPHERE")}'
        return zone
