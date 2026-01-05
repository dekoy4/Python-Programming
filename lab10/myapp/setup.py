from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

setup(
    name="lab10-integration",
    ext_modules=cythonize(
        ["cython/integrate_cython.pyx"],
        compiler_directives={'language_level': "3"},
        annotate=True  # Создает HTML отчет
    ),
    include_dirs=[numpy.get_include()],
    zip_safe=False,
)
