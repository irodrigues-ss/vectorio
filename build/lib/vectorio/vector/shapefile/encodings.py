#!-*-coding:utf-8-*-

import os
import warnings
from vectorio.vector.exceptions import CharDecodeError


SHAPEFILE_ENCODINGS = {
    'LATIN1': 'ISO-8859-1', 'LATIN3': 'ISO-8859-3', 'UTF-8': 'UTF-8',
    'ISO-8859-2': 'ISO-8859-2'
}
ANY_INDEX = 4


class ShapeEncodings:

    _raise_exception = None

    def __init__(self, raise_exception=True):
        self._raise_exception = raise_exception

    def _accepted_shape_encodings(self):
        return str(
            list(
                SHAPEFILE_ENCODINGS.values()
            )
        ).replace("'", "").replace("[", "").replace("]", "")

    def _validate_encoding(self, fpath_dbf: str, encoding: str):
        with open(fpath_dbf, encoding=encoding) as fdbf:
            fdbf.read()[0:ANY_INDEX]

    def from_file(self, fpath_dbf: str) -> str:
        encoding = SHAPEFILE_ENCODINGS['UTF-8']
        try:
            self._validate_encoding(fpath_dbf, encoding)
        except UnicodeDecodeError:
            encoding = SHAPEFILE_ENCODINGS['LATIN1']
            self._validate_encoding(fpath_dbf, encoding)
        except UnicodeDecodeError:
            encoding = SHAPEFILE_ENCODINGS['LATIN3']
            self._validate_encoding(fpath_dbf, encoding)
        except UnicodeDecodeError:
            encoding = SHAPEFILE_ENCODINGS['ISO-8859-2']
            self._validate_encoding(fpath_dbf, encoding)
        except Exception as ex:
            MSG = f"Erro on read {fpath_dbf}. Please, check if the " \
                f"{fpath_dbf} file exists and check the encoding " \
                "character of the .dbf.\n" \
                f"Accepted encodings: {self._accepted_shape_encodings()}."\
                f"Inner Exception: {str(ex)}"

            if self._raise_exception:
                raise CharDecodeError(MSG)

        return encoding
