#!-*-coding:utf-8-*-

import os


def get_root_project(directory):
    path = os.path.abspath(directory)
    if os.path.isdir(path):
        if "vectorio" in os.listdir(path):
            return path
        else:
            return get_root_project(os.path.dirname(path))
    else:
        return get_root_project(os.path.dirname(path))


ROOT_PROJECT = get_root_project(__file__)
STATIC_DIR = os.path.join(ROOT_PROJECT, 'vectorio', '_assets')
