#!-*-coding:utf-8-*-
import os
from abc import ABC
from vectorio.vector.metrics.vertices import Vertices


class IVector(ABC):

    def vertices_by_feature(self, ds):
        vertices = Vertices()
        lyr = ds.GetLayer(0)
        vertices_count = {}
        for feat_idx in range(lyr.GetFeatureCount()):
            feat = lyr.GetFeature(feat_idx)
            geom = feat.geometry()
            feat_id = f'Feature_{feat_idx}_{geom.GetGeometryName()}'
            vertices_count[feat_id] = vertices.tell(geom)
        return vertices_count

    def _validate_basedir(self, out_path: str):
        dirname = os.path.dirname(out_path)
        if dirname != '':
            if not os.path.exists(dirname):
                raise DirectoryDoesNotExists(
                    f'The directory "{dirname}" does not exists.'
                )
