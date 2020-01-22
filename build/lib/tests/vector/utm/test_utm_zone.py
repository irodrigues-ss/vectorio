#!-*-coding:utf-8-*-

from vectorio.vector import WKT, VectorReprojected, UTMZone


class TestUTMZone:

    def setup_method(self):
        self.utm = UTMZone()
        self.ds_wkt = VectorReprojected(WKT(), out_srid=4326).datasource('POLYGON((-73.79131452179155 -11.78691590735885,-27.12139264679149 -12.645910804419744,-47.46330883419978 10.894322081983276,-73.79131452179155 -11.78691590735885))')
        self.exp_zones = {'20NW', '24NW', '19SW', '23SW', '25SW', '23NW', '26SW', '22SW', '24SW', '20SW', '21SW', '18SW', '21NW', '22NW'}

    def test_zone_from_biggest_geom(self):
        assert self.utm.zone_from_biggest_geom(
            self.ds_wkt
        ) == '22SW'

    def test_zones(self):
        zones = self.utm.zones(self.ds_wkt)
        for exp_zone in self.exp_zones:
            assert exp_zone in zones
