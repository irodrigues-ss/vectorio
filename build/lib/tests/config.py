#!-*-coding:utf-8-*-

import os
from vectorio.config import ROOT_PROJECT

TESTS_DIRPATH = os.path.join(ROOT_PROJECT, 'tests')
FIXTURES_DIRPATH = os.path.join(TESTS_DIRPATH, 'fixtures')
FILESDIR_FROM_FIXTURES = os.path.join(FIXTURES_DIRPATH, 'files')


def get_test_file(fname: str):
    return os.path.join(FILESDIR_FROM_FIXTURES, fname)
