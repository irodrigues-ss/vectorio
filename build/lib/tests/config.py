#!-*-coding:utf-8-*-

import os


def get_root(directory):
    dirname = os.path.dirname(directory)
    if 'setup.py' in os.listdir(dirname):
        return dirname
    else:
        return get_root(dirname)


ROOT_PROJECT = get_root(__file__)

TESTS_DIRPATH = os.path.dirname(__file__)
FIXTURES_DIRPATH = os.path.join(TESTS_DIRPATH, 'fixtures')
FILESDIR_FROM_FIXTURES = os.path.join(FIXTURES_DIRPATH, 'files')
