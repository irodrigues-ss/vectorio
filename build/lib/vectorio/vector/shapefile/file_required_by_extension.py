#!-*-coding:utf-8-*-

import os
import copy

from vectorio.vector.exceptions import FileNotFound
from vectorio.vector.shapefile.interfaces.ifile_required_by_extension import (
    IFileRequiredByExtension
)


class FileRequiredByExtension(IFileRequiredByExtension):

    def __init__(self, dirpath: str, expected_ext_list: list):
        self._dirpath = dirpath
        self._expected_ext_list = expected_ext_list

    def _validate_found_ext(self, found_ext: list):
        """
        This method will check if the required files are found. Case the some
        file is missing, a exception will be raised.
        """
        missing_files = list(set(self._expected_ext_list) - set(found_ext))
        if len(missing_files) != 0:
            raise FileNotFound(f"File .{''.join(missing_files)} not found.")

    def _files_by_ext(self) -> dict:
        """
        This method will iterate by directory (dirpath) for search (recursivly)
        the files by extension.
        """
        def find_recursivly(dirpath, ext_lst):
            found_files_by_ext = {}  # result of this method
            missing_files = copy.copy(ext_lst)  # list of extension from shapefile

            for fname in os.listdir(dirpath):
                fpath = os.path.join(dirpath, fname)

                if len(missing_files) == 0:
                    return found_files_by_ext

                if os.path.isdir(fpath):
                    return find_recursivly(fpath, missing_files)
                else:
                    ext = fname.split('.')[-1].lower()
                    if ext in missing_files:  # found extension
                        missing_files.pop(missing_files.index(ext))
                        found_files_by_ext[ext] = fpath
            return found_files_by_ext

        return find_recursivly(self._dirpath, self._expected_ext_list)

    def files(self):
        files = self._files_by_ext()
        self._validate_found_ext(files.keys())
        return files

    def __repr__(self):
        return '<FileRequiredByExtension>'
