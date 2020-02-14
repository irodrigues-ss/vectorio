#!-*-coding:utf-8-*-

import os
from vectorio.vector.exceptions import ErrorOnReadDBF


SHAPEFILE_ENCODINGS = {
    'LATIN1': 'ISO-8859-1',
    'LATIN3': 'ISO-8859-3',
    'UTF-8': 'UTF-8'
}

os.environ['SHAPE_ENCODING'] = SHAPEFILE_ENCODINGS['UTF-8']
ANY_INDEX = 4


class ShapeEncodings:

    def _accepted_shape_encodings(self):
        return str(
            list(
                SHAPEFILE_ENCODINGS.values()
            )
        ).replace("'", "").replace("[", "").replace("]", "")

    def define_encoding(self, fpath: str):
        # TODO: Create unities tests for this method
        fpath_dbf = fpath.replace('.shp', '.dbf')
        with open(fpath_dbf) as fdbf:
            try:
                fdbf.read()[0:ANY_INDEX]
            except UnicodeDecodeError:
                os.environ['SHAPE_ENCODING'] = SHAPEFILE_ENCODINGS['LATIN1']
                fdbf.read()[0:ANY_INDEX]
            except UnicodeDecodeError:
                os.environ['SHAPE_ENCODING'] = SHAPEFILE_ENCODINGS['LATIN3']
                fdbf.read()[0:ANY_INDEX]
            except Exception:
                raise ErrorOnReadDBF(
                    f"Erro on read {fpath_dbf}. Please, check if the "\
                        f"{fpath_dbf} file exists and check the encoding "\
                        "character of the .dbf.\n" \
                        f"Accepted encodings: {self._accepted_shape_encodings()}."
                )