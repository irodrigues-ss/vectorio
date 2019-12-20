

class Vertices:

    _FUNC_FOR_COUNT_VERTICES = {}

    def __init__(self):
        # "switch" method for count vertices
        self._FUNC_FOR_COUNT_VERTICES = {
            'POINT': self._point,
            'LINESTRING': self._line,
            'POLYGON': self._polygon,
            'MULTIPOINT': self._multipoint,
            'MULTILINESTRING': self._multiline,
            'MULTIPOLYGON': self._multipolygon
        }

    def _multiline(self, geom):
        vertices = []
        for idx_geom in range(geom.GetGeometryCount()):
            vertices.append(geom.GetGeometryRef(idx_geom).GetPointCount())
        return vertices

    def _multipoint(self, geom):
        vertices = []
        for idx_geom in range(geom.GetGeometryCount()):
            vertices.append(geom.GetGeometryRef(idx_geom).GetPointCount())
        return vertices

    def _multipolygon(self, geom):
        vertices = []
        rings = []
        for idx_geom in range(geom.GetGeometryCount()):
            polygon = geom.GetGeometryRef(idx_geom)
            rings = []
            for idx_ring in range(polygon.GetGeometryCount()):
                ring = polygon.GetGeometryRef(idx_ring)
                #print(ring.GetPointCount())
                rings.append(ring.GetPointCount())
            vertices.append(rings)
        return vertices

    def _point(self, geom):
        vertices = []
        vertices.append(geom.GetPointCount())
        return vertices

    def _line(self, geom):
        vertices = []
        vertices.append(geom.GetPointCount())
        return vertices

    def _polygon(self, geom):
        vertices = []
        for idx_geom in range(geom.GetGeometryCount()):
            vertices.append(geom.GetGeometryRef(idx_geom).GetPointCount())
        return vertices

    def tell(self, geom):
        vertices_counter = self._FUNC_FOR_COUNT_VERTICES.get(geom.GetGeometryName())
        if vertices_counter is None:
            raise Exception('')
        return vertices_counter(geom)
