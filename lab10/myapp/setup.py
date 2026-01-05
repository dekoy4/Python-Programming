from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "cython/integrate_cython.pyx",
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False
        },
        annotate=True
    )
)
