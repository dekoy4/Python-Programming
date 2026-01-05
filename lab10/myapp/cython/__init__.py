"""
Cython оптимизированные модули интегрирования.
Импорт доступен только после компиляции: python setup.py build_ext --inplace
"""

try:
    from .integrate_cython import (
        integrate_cython_py,
        integrate_cos_cython, 
        integrate_sin_cython,
        integrate_nogil_py
    )
    
    # Публичный API Cython модуля
    __all__ = [
        'integrate_cython_py',
        'integrate_cos_cython',
        'integrate_sin_cython',
        'integrate_nogil_py'
    ]
    
except ImportError:
    print("Cython модули не скомпилированы.")
    print("Выполните: python setup.py build_ext --inplace")
    __all__ = []
