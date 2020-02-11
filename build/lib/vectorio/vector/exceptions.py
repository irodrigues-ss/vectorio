#!-*-coding:utf-8-*-


class FileNotFound(Exception):
    pass


class GeojsonInvalid(Exception):
    pass


class WKTInvalid(Exception):
    pass


class GeometryTypeInvalid(Exception):
    pass


class DataSourceWithoutSpatialRef(Exception):
    pass


class TypeFromFileIsNotSupported(Exception):
    pass


class ShapefileInvalid(Exception):
    pass


class ShapefileIsEmpty(Exception):
    pass


class DirectoryDoesNotExists(Exception):
    pass


class ImpossibleCreateShapefileFromGeometryCollection(Exception):
    pass


class ErrorOnIntersection(Exception):
    pass


class ExistsManyGeometriesTypes(Exception):
    pass
