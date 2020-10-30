# Vector IO - Geoprocessing utility for working with vector data.
## \> Deprecated README. In the next version will be create new Readme.<
## Requirements
- python >= 3.6
- gdal >= 2.2
- rar
- unrar

## Description
This project is a tool for working with vectorial data based on [GDAL](https://gdal.org/). This tool is an envelope about gdal and aims to work with different types of vector data quickly, intelligently, and simply. The vectorIO provide the support for (read and write) geojson, wkt and Shapefile, support for quickly switching between different spatial data types, and provides a exception handler for warnings from gdal.

## Installation

#### Docker

- Complete enviroment on Ubuntu: [Dockerfile](https://github.com/igor-rodrigues-ss/vectorio/blob/master/Dockerfile)

Creating a image and instantiate the container:

```shell
# access the directory where is the Dockerfile
docker image build -t vectorio-env:001 . # build the image
# vectorio-env:001 - can be any name with the version of the your preference
docker container run -it vectorio-env:001 # instantiate a new container
```

#### Ubuntu 18.04

- Rar

```shell
apt-get install rar unrar
```

- Gdal

[Installing gdal on ubuntu](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)

- Gdal for python
```shell
gdalinfo --version
pip3 install gdal==<gdal_version>
```

## Features
- [Read and write geojson](#read-and-write-geojson)
- [Read and write WKT](#read-and-write-wkt)
- [Read and write Shapefile](#read-and-write-wkt)
- [Reprojecting a vector](#reprojecting-a-vector)
- [Quickly switching between geographic data](#quickly-switching-between-geographic-data)
- [Search UTM Zone from Geometry](#search-utm-zone-from-geometry)
- [Raise exception for warnings from gdal](#raise-exception-for-warnings-from-gdal)
- [Reprojecting a datasource directly](#reprojecting-a-datasource-directly)
- [Counting Vertices](#counting-vertices)

#### Read and Write Geojson

Working with geojson data and geojson file. By default, the datasource is created as WGS84.

- Preparing the data

```python
from vectorio.vector import Geojson
data = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Polygon","coordinates": [[[-44.89013671875,-6.577303118123875],[-46.29638671874999,-7.460517719883772],[-44.4287109375,-7.318881730366743],[-44.89013671875,-6.577303118123875]]]}}]}'
gjs = Geojson()
```

- Read all data

```python
ds = gjs.datasource(data)
gjs.collection(ds)
```

- Reading and iterating over each feature

```python
ds = gjs.datasource(data)
for item in gjs.items(ds):
    print(item)
```

- Creating a new geojson file

```python
ds = gjs.datasource(data)
gjs.write(ds, 'data.geojson')
```

- Reading from geojson file

```python
from vectorio.vector import GeoData
gf_gjs = GeoData(gjs)
ds = gf_gjs.datasource('data.geojson')
gf_gjs.collection(ds)
```

<br/>

#### Read and write WKT

Working with wkt data and wkt file. Is supported geometry collection and single geometries. By default, the datasource is created as WGS84.

The wkt object has some parameters:

```python
WKT(as_geometry_collection=True, srid=4326)
```
- *as_geometry_collection*: return a geometry collection same when the data is a single geometry by method *collection*.
- *srid*: Initial SRID for WKT.

- Preparing the data

```python
from vectorio.vector import WKT
data = "GEOMETRYCOLLECTION(POINT(-48.740641051554974 -9.249606262178954), LINESTRING(-50.278726989054974 -11.023166202413554,-48.608805114054974 -10.375450023701761))"
wkt = WKT()
```

- Read all data

```python
ds = wkt.datasource(data)
wkt.collection(ds)
```

- Reading and iterating over each geometry

```python
ds = wkt.datasource(data)
for item in wkt.items(ds):
    print(item)
```

- Creating a new wkt file

```python
ds = wkt.datasource(data)
wkt.write(ds, 'data.wkt')
```

- Reading from wkt file

```python
from vectorio.vector import GeoData
gf_wkt = GeoData(wkt)
ds = gf_wkt.datasource('data.wkt')
gf_wkt.collection(ds)
```

<br/>

#### Read and write Shapefile

Working with read and write shapefile. Is supported shapefiles compressed as .zip and .rar. By default, the datasource is created as based on projection present on .prj file. *obs: read and write of the .rar files is available only for linux OS. Only the ShapefileAsRar class has this restriction. The other classes are available for any OS.*

- Preparing the data

```python
from vectorio.vector import Shapefile
shape = Shapefile()
```

- Read all data from .shp file

```python
ds = shape.datasource('data.shp')
shape.collection(ds)
```

- Reading and iterating over each feature from .shp file

```python
ds = shape.datasource('data.shp')
for item in shape.items(ds):
    print(item)
```

- Creating a new shapefile (Are be created the files .shp, .shx, .dbf, .prj)

```python
ds = shape.datasource('data.shp')
shape.write(ds, 'out.shp')
# >>> out.shp
```

##### Read and write Shapefile compressed

By default the algorithm will search recusivly the files .shp, .shx, .dbf, .prj inside of the compressed file. The algorithm will search the first file of the each extension, case the compressed file contains 2 (or more) .shp files, or 2 (or more) .prj file, will be obtained the first .shp file and the first .prj file. 

- Processing from zip

```python
from vectorio.vector import Shapefile, ShapefileAsZip
shape = ShapefileAsZip(Shapefile())
ds = shape.datasource('data.zip') # creating a datasource
shape.collection(ds)  # read all data

for item in shape.items(ds):  # iterating over each item
    print(item)

shape.write(ds, 'out.zip') # Creating a shapefile compressed as .zip
# >>> out.zip
```

- Processing from .rar (*available only for linux OS*)

```python
from vectorio.vector import Shapefile, ShapefileAsRar
shape = ShapefileAsRar(Shapefile())
ds = shape.datasource('data.rar') # creating a datasource
shape.collection(ds)  # read all data

for item in shape.items(ds):  # iterating over each item
    print(item)

shape.write(ds, 'out.rar') # Creating a shapefile compressed as .rar
# >>> out.rar
```

<br/>

#### Reprojecting a Vector

The spatial reprojection works with same geography type thats implements the interface IVectorIO.
If the input srid (in_srid) are be ommited, will used the srid from geometry.

- Reprojecting a shapefile

```python
from vectorio.vector import Shapefile, ShapefileAsZip, VectorIOReprojected
shape = VectorIOReprojected(
    ShapefileAsZip(Shapefile()), in_srid=31982, out_srid=4674
)
ds = shape.datasource('data_utm22.zip')

shape.collection(ds)  # read all data

for item in shape.items(ds):  # iterating by each feature
    print(item)

shape.write(ds, 'data_reprojected.zip')  # creating a new shapefile
```

- Reprojecting a WKT

By default the wkt is in WGS84 spatial reference.

```python
from vectorio.vector import WKT, VectorIOReprojected
wkt = VectorIOReprojected(WKT(), out_srid=31982)
ds = wkt.datasource('POLYGON((-49.698036566343376 -9.951372897703846,-51.148231878843376 -11.591810720955946,-48.467567816343376 -11.763953408065282,-49.698036566343376 -9.951372897703846))')

wkt.collection(ds)  # read all data

for item in wkt.items(ds):  # iterating by each geometry
    print(item)

wkt.write(ds, 'data-reprojected.wkt')  # creating a new wkt file
```

- Reprojecting a Geojson

By default the geojson is in WGS84 spatial reference.

```python
from vectorio.vector import Geojson, VectorIOReprojected
gjs = VectorIOReprojected(Geojson(), out_srid=31982)
ds = gjs.datasource('{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Polygon","coordinates": [[[-45.992889404296875,-9.654907854199012],[-46.12884521484374,-9.72259300616733],[-45.96954345703125,-9.738835407948073],[-45.992889404296875,-9.654907854199012]]]}}]}')

gjs.collection(ds)  # read all data

for item in gjs.items(ds):  # iterating by each feature
    print(item)

gjs.write(ds, 'data-reprojected.geojson')  # creating a new geojson file
```

<br/>

#### Quickly Switching Between Geographic Data

For execution of the Quick switch must be used the *VectorComposite* present on package *vectorio.vector*.

```python
VectorComposite(input_vector_obj, ouput_vector_obj)
```

##### Quick switch from geojson to wkt 

- Preparing data

```python
from vectorio.vector import Geojson, WKT, VectorComposite
data = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Polygon","coordinates": [[[-44.89013671875,-6.577303118123875],[-46.29638671874999,-7.460517719883772],[-44.4287109375,-7.318881730366743],[-44.89013671875,-6.577303118123875]]]}}]}'
vector = VectorComposite(Geojson(), WKT())
```

- Reading all geometry from geojson as wkt

```python
vector.collection(data)
```

- Iterating over all geometries as wkt

```python
for geom_wkt in vector.items(data):
    print(geom_wkt)
```

- Creating a wkt file

```python
vector.write(data, 'output.wkt')
```

##### Quick switch from wkt to shapefile as zip

```python
from vectorio.vector import Shapefile, ShapefileAsZip, WKT, VectorComposite
data = 'MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))'
vector = VectorComposite(WKT(), ShapefileAsZip(Shapefile()))
```

- Reading all geometry from wkt

```python
vector.collection(data)
```

- Iterating over all geometries

```python
for geom in vector.items(data):
    print(geom)
```

- Creating a shapefile as zip

```python
vector.write(data, 'output.zip')
```

##### Search UTM Zone from Geometry

- This functionality will search the UTM Zone from some geometry.

```python
from vectorio.vector import UTMZone, VectorIOReprojected, WKT
ds_wkt = VectorIOReprojected(WKT(), out_srid=4326).datasource('POLYGON((-73.79131452179155 -11.78691590735885,-27.12139264679149 -12.645910804419744,-47.46330883419978 10.894322081983276,-73.79131452179155 -11.78691590735885))')
utm = UTMZone()
utm.zones(ds_wkt) # getting all UTM Zones that intersect with the geometry
```

- The method **zone_from_biggest_geom** get only one zone that has the biggest geometry. For example, if a large geometry is in UTM Zone 25N or 26N, this method will calculate the area (for polygon) or length (for line) of geometry and return the UTM Zone where the area or length is the biggest.

- **Signature**: *zone_from_biggest_geom(self, inp_ds: DataSource, wkt_prj_for_metrics: str, in_wkt_prj=PRJ_WGS84)*
    - *wkt_prj_for_metrics*: required
    - *inp_ds*: required
    - *in_wkt_prj*: Optional. Used case the input datasource no has a CRS.

```python
# out_wkt_prj - necessary for make metrics calculations
out_wkt_prj = 'PROJCS["Brazil / Albers Equal Area Conic (WGS84)",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["longitude_of_center",-50.0],PARAMETER["standard_parallel_1",10.0],PARAMETER["standard_parallel_2",-40.0],PARAMETER["latitude_of_center",-25.0],UNIT["Meter",1.0]]'
utm.zone_from_biggest_geom(ds_wkt, out_wkt_prj=out_wkt_prj) # getting one UTM Zone
```

- Points are ignored in this calculation. This method isn't remomended for geometries composed only by Points, (MultiPoint, GeometryCollection of points e etc.), because, the UTM zone returned is based in area/lenth metrics. Soon, will be implemented a method for get UTM Zone only for Point Geometries. 

<br/>

#### Raise Exception for Warnings From Gdal

For use the exception from gdal warnings should use the decorator
*gdal_warning_as_exception* presents on *vectorio.gdal* package. This decorator will throw the error when the *IsValid()* method from *geometry()* method will be used.

```python
from vectorio.gdal import gdal_warning_as_exception
from vectorio.vector import WKT

self_intersect_polygon = 'POLYGON((-54.24438490181399 -5.466896872158672,-54.84863294868899 -5.882330540835073,-54.09057630806399 -5.8714019542356475,-54.83764662056399 -5.379399666352095,-54.24438490181399 -5.466896872158672))'

@gdal_warning_as_exception
def possible_error():
    wkt = WKT()
    ds = wkt.datasource(self_intersect_polygon)
    lyr = ds.GetLayer(0)
    feat = lyr.GetFeature(0)
    feat.geometry().IsValid()

possible_error()
# >>> GDALSelfIntersectionGeometry: Self-intersection at or near point -54.469636435829948 -5.6217621987992636
```

##### Possibles exceptions
- *GDALSelfIntersectionGeometry*: Exception throwed when a polygon contains a self intersection.  
- *GDALBadClosedPolygon*: Exception throwed when a polygon not correctly close.
- *GDALUnknownException*: Exception throwed when occurs a unknown error.

**Obs:** All the exceptions are available on package *vectorio.exceptions*

#### Reprojecting a datasource directly

- To make spatial reprojection use the class VectorIOReprojected [metioned above](#reprojecting-a-vector). However, in same moment will be necessary reproject a datasource directly, for this use the DataSourceReprojected class.

- **Signature**: *DataSourceReprojected(inp_ds: DataSource, in_srid: int=None, out_srid: int=None, in_wkt_prj=None, out_wkt_prj=None, use_wkt_prj: bool=False)*
    - **inp_ds**: required. Datasource that will be reprojected.
    - **in_srid**: optional. Used case the input datasource not has a CRS. (Used only when the flag **use_wkt_prj** is *False*).
    - **out_srid**: Required whether the **use_wkt_prj** is *False*.
    - **in_wkt_prj**: optional. WKT Projection on OGC pattern. Used case the input datasource not has a CRS. (Used only when the flag **use_wkt_prj** is *True*).
    - **out_wkt_prj**: Required whether the **use_wkt_prj** is *True*. WKT Projection on OGC pattern.
    - **use_wkt_prj**: Boolean to define whether the datasource will be reprojected with SRID our with the WKT Projection.

- Methods:
    - **ref() -> DataSource**: Return the DataSource reprojected.

- Reprojecting with SRID.

```python
from vectorio.vector import WKT, DataSourceReprojected
wkt = WKT()
ds = wkt.datasource('POLYGON((-45.522540331834634 -6.851736627227062,-47.016680956834634 -7.7670786428296275,-45.434649706834634 -8.332736100352385,-45.522540331834634 -6.851736627227062))')
ds1 = DataSourceReprojected(ds, out_srid=31983).ref()
wkt.collection(ds1)
```
- Reprojecting with WKT Projection.

```python
from vectorio.vector import WKT, DataSourceReprojected
wkt = WKT()
prj = 'PROJCS["SIRGAS 2000 / UTM zone 23S",GEOGCS["SIRGAS 2000",DATUM["Sistema_de_Referencia_Geocentrico_para_America_del_Sur_2000",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6674"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4674"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-45],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",10000000],AUTHORITY["EPSG","31983"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
ds = wkt.datasource('POLYGON((-45.522540331834634 -6.851736627227062,-47.016680956834634 -7.7670786428296275,-45.434649706834634 -8.332736100352385,-45.522540331834634 -6.851736627227062))')
ds2 = DataSourceReprojected(ds, out_wkt_prj=prj, use_wkt_prj=True).ref()
wkt.collection(ds2)
```

#### Counting Vertices

All classes that are vector has the method for count all vertices. Below, are be exemplified
 with a WKT, however, this method works with Shapefile, GeoJson too.

- **Signature**: *vertices_by_feature(ds: DataSource) -> dict*
    - ds: Required. DataSource for count your vertices.

- **Return**:
    - Will be returned a dictionary of vertices by feature.

```python
from vectorio.vector import WKT
wkt = WKT() 
ds = wkt.datasource('POLYGON((-45.522540331834634 -6.851736627227062,-47.016680956834634 -7.7670786428296275,-45.434649706834634 -8.332736100352385,-45.522540331834634 -6.851736627227062))')
wkt.vertices_by_feature(ds) # works with shapefile or Geojson 
# shapefile_obj.vertices_by_feature() or geojson_obj.vertices_by_feature()
```
