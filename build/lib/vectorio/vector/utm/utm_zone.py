#!-*-coding:utf-8-*-
import os
from osgeo import ogr
from osgeo.ogr import DataSource, CreateGeometryFromWkt, Feature
from vectorio.compress.zip_file import Zip
from vectorio.vector import (
    Shapefile, ShapefileCompressed, WKT
)
from vectorio.config import STATIC_DIR
from vectorio.vector.exceptions import (
    ErrorOnIntersection, ExistsManyGeometriesTypes, DataSourceNotIntersectsWithAnyUTMZones
)
from vectorio.config import GDAL_DRIVERS_NAME, PRJ_WGS84
from vectorio.vector import DataSourceReprojected
from typeguard import typechecked
from vectorio.vector.exceptions import ImpossibleFindUTMZoneGeometryHasSelfIntersection


class UTMZone:

    _drv_mem = None
    _world_utm_grid_ds = None

    def __init__(self):
        os.environ['SHAPE_ENCODING'] = 'ISO-8859-3'
        self._world_utm_grid = ShapefileCompressed(
            Shapefile(os.path.join(STATIC_DIR, 'World_UTM_Grid_HM.zip'), search_encoding=False), compress_engine=Zip()
        )
        self._drv_mem = ogr.GetDriverByName(GDAL_DRIVERS_NAME['MEMORY'])

    def _zone_value(self, feat: Feature):
        return f'{feat.GetFieldAsInteger("ZONE")}{feat.GetFieldAsString("HEMISPHERE")}'

    @typechecked
    def zones_from_iteration(self, wkt_data: str) -> set:
        """
        Alternative method for get UTM Zones whether The geometry has a topology
        error that to prevent the gdal from execute Layer.Intersection method.
        :param: wkt_data: str
        :return: set
            set with UTM Zones numbers and Hemisphere
        """
        geom = CreateGeometryFromWkt(wkt_data)
        ds_utm_grid = self._world_utm_grid.datasource()
        lyr_utm_grid = ds_utm_grid.GetLayer()
        utm_zones = set()
        for feat in lyr_utm_grid:
            geom_utm_zone = feat.geometry()
            if geom.Intersects(geom_utm_zone):
                utm_zones.add(self._zone_value(feat))
        lyr_utm_grid.ResetReading()
        return utm_zones

    def _intersection_ds(self, ds_utm: DataSource, inp_ds: DataSource):
        lyr_utm = ds_utm.GetLayer(0)
        target_lyr = inp_ds.GetLayer(0)

        ds_out = self._drv_mem.CreateDataSource('out_mem_ds')
        lyr_out = ds_out.CreateLayer('out_mem_Lyr')
        intersection = lyr_utm.Intersection(target_lyr, lyr_out)

        if intersection == 6:
            raise ImpossibleFindUTMZoneGeometryHasSelfIntersection(
                'Impossible find UTM Zone. The geometry has a topology error (Self Instersection). Please use the method "zones_from_iteration".'
            )
        elif intersection != 0:
            raise ImpossibleFindUTMZone(
                "Impossible find UTM Zone. Please, check if you has a valid geometries."
            )
        return ds_out

    @typechecked
    def zones(self, inp_ds: DataSource) -> set:
        ds = self._intersection_ds(self._world_utm_grid.datasource(), inp_ds)
        lyr = ds.GetLayer(0)
        result = set()

        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            result.add(self._zone_value(feat))
        return result

    @typechecked
    def zone_from_biggest_geom(self, inp_ds: DataSource, wkt_prj_for_metrics: str, in_wkt_prj=PRJ_WGS84):
        inter_ds = self._intersection_ds(self._world_utm_grid.datasource(), inp_ds)
        inter_lyr = inter_ds.GetLayer()

        if inter_lyr.GetFeatureCount() == 0:
            raise DataSourceNotIntersectsWithAnyUTMZones(
                'The datasource not intersect with UTM Zones. Please, check '
                'if "in_wkt_prj" is equivalent to Datum from datasource. Use '
                'Datuns for this operations.'
            )

        ds = DataSourceReprojected(
            inter_ds, in_wkt_prj=in_wkt_prj,
            out_wkt_prj=wkt_prj_for_metrics, use_wkt_prj=True
        ).ref()
        biggest_part_idx = 0
        indexes_from_feats = []  # all indexes from features
        metrics = []  # area or length of the geometry from feature
        lyr = ds.GetLayer(0)

        for idx_feat in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(idx_feat)
            geom_type = feat.geometry().GetGeometryName()
            area_or_length = 0
        
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
        feat = lyr.GetFeature(biggest_part_idx) # big geometry
        zone = f'{feat.GetFieldAsInteger("ZONE")}{feat.GetFieldAsString("HEMISPHERE")}'
        return zone
