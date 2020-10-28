

class Vertices:

    _FUNC_FOR_COUNT_VERTICES = {}

    def __init__(self):
        # "switch" useful for map the methods for count vertices by geometry types
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
        for idx_geom in range(geom.GetGeometryCount()):
            polygon = geom.GetGeometryRef(idx_geom)
            rings = []
            for idx_ring in range(polygon.GetGeometryCount()):
                ring = polygon.GetGeometryRef(idx_ring)
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
        gtype = geom.GetGeometryName()
        vertices_counter = self._FUNC_FOR_COUNT_VERTICES.get(gtype)
        if vertices_counter is None:
            raise Exception(f'Function for count vertices of {gtype} not found.') # TODO: Create as custom exception
        return vertices_counter(geom)
