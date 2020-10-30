#!-*-coding:utf-8-*-

from vectorio.vector import WKT, VectorReprojected, UTMZone


PRJ_SIRGAS2000 = 'GEOGCS["SIRGAS 2000",DATUM["Sistema_de_Referencia_Geocentrico_para_America_del_Sur_2000",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6674"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4674"]]'
ALBERS = 'PROJCS["Brazil / Albers Equal Area Conic (WGS84)",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["longitude_of_center",-50.0],PARAMETER["standard_parallel_1",10.0],PARAMETER["standard_parallel_2",-40.0],PARAMETER["latitude_of_center",-25.0],UNIT["Meter",1.0]]'


class TestUTMZone:

    def setup_method(self):
        self.utm = UTMZone()
        self.ds_wkt = VectorReprojected(
            WKT('POLYGON((-73.79131452179155 -11.78691590735885,-27.12139264679149 -12.645910804419744,-47.46330883419978 10.894322081983276,-73.79131452179155 -11.78691590735885))'),
            out_srid=4326
        ).datasource()
        self.exp_zones = {'20NW', '24NW', '19SW', '23SW', '25SW', '23NW', '26SW', '22SW', '24SW', '20SW', '21SW', '18SW', '21NW', '22NW'}

    def test_zone_from_biggest_geom(self):
        assert self.utm.zone_from_biggest_geom(
            self.ds_wkt, in_wkt_prj=PRJ_SIRGAS2000, wkt_prj_for_metrics=ALBERS
        ) == '22SW'

    def test_zones(self):
        zones = self.utm.zones(self.ds_wkt)
        for exp_zone in self.exp_zones:
            assert exp_zone in zones

    def test_zones_from_iteration(self):
        wkt_self_intersect = WKT('POLYGON((-47.49821977864582 -16.544385736231273,-47.60533647786457 -16.589139362122044,-47.64928179036457 -16.557549646684464,-47.619210387984424 -16.708802309521275,-47.545052673140674 -16.727215738350523,-47.501107360640674 -16.67460122975974,-47.440682555953174 -16.64302557351627,-47.440682555953174 -16.703541003478303,-47.465401794234424 -16.695648772583993,-47.388497497359424 -16.679863332707583,-47.413216735640674 -16.47453441997014,-47.49821977864582 -16.544385736231273))')
        zone = self.utm.zones_from_iteration(wkt_self_intersect.geometry_collection())
        assert zone == {'23SW'}
