"""
Лабораторная работа 10: Методы оптимизации вычисления интегралов.
Сравнение производительности: Python → Потоки → Процессы → Cython → noGIL.
"""

from .integrate import integrate
from .integrate_async import integrate_threads, integrate_processes

# Публичный API пакета
__all__ = [
    'integrate',
    'integrate_threads', 
    'integrate_processes'
]

# Версия пакета
__version__ = '1.0.0'
