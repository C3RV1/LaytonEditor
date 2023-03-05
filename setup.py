import numpy
from setuptools import setup
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    ext_modules=cythonize("formats/sound/compression/*.pyx",
                          include_path=[numpy.get_include()],
                          annotate=True),
    include_dirs=[numpy.get_include()],
    zip_safe=False
)
