import pybind11
from setuptools import setup, Extension
from setuptools import find_packages

ext_modules = [
    Extension(
        name="pyta.smoothing_cpp",  # Build directly into pyta/
        sources=[
            "native/cpp/binding.cpp",
            "native/cpp/smoothings.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    )
]

setup(
    name="native_cpp",
    version="0.1.1",
    packages=find_packages(include=["pyta", "pyta.*"]),
    ext_modules=ext_modules,
    zip_safe=False,
)
