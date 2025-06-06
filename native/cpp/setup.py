from setuptools import setup, Extension
import pybind11
import sys
import os

from distutils.sysconfig import get_config_vars
for var in ['OPT', 'CFLAGS', 'BASECFLAGS']:
    if var in get_config_vars():
        get_config_vars()[var] = ""

ext_modules = [
    Extension(
        name='smoothing_cpp',
        sources=['smoothings.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++17'],
    ),
]

setup(
    name='smoothing_cpp',
    version='0.1',
    ext_modules=ext_modules,
)
