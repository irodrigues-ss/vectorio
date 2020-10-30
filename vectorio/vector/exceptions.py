#!-*-coding:utf-8-*-


class ImpossibleFindUTMZone(Exception):
    pass


class ImpossibleFindUTMZoneGeometryHasSelfIntersection(ImpossibleFindUTMZone):
    pass


class InvalidOperationForThisDataType(Exception):
    pass


class KMLInvalid(Exception):
    pass


class ShapefilePathWasntPassed(Exception):
    pass


class CharDecodeError(Exception):
    pass


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


class DataSourceNotIntersectsWithAnyUTMZones(Exception):
    pass


class SRIDNotFound(Exception):
    pass


class WKTPRJNotFound(Exception):
    pass