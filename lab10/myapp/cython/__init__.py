"""
Cython модули через pyximport (работает без setup.py)
"""
import pyximport
pyximport.install()

from .integrate_cython import integrate_cos_cython, integrate_python
__all__ = ['integrate_cos_cython', 'integrate_python']
