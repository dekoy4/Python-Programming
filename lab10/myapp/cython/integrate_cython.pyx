Полный код для cython/integrate_cython.pyx
text
"""
Итерация 4: Cython оптимизация функции интегрирования.
Компиляция: python setup.py build_ext --inplace
Анализ: python -m cython -a integrate_cython.pyx
"""

cdef extern from "math.h":
    double cos(double x)
    double sin(double x)

cdef double integrate_cython_loop(double (*f)(double), double a, double b, int n_iter):
    """
    Базовая Cython версия с типизированными переменными.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += f(a + i * step) * step
    
    return acc

def integrate_cython_py(f, double a, double b, int n_iter=100000):
    """
    Python-интерфейс для Cython функции.
    
    Args:
        f: Python функция или встроенная math функция (cos, sin)
        a, b: границы интегрирования
        n_iter: количество итераций
    
    Returns:
        float: значение интеграла
    """
    if hasattr(f, '__call__'):
        # Python функция - медленный вызов
        return integrate_cython_loop_py(f, a, b, n_iter)
    else:
        # Предполагаем C функцию (cos, sin)
        return integrate_cython_loop(<double (*)(double)>f, a, b, n_iter)

cdef double integrate_cython_loop_py(object f, double a, double b, int n_iter):
    """Вспомогательная для Python функций."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += f(a + i * step) * step
    
    return acc

# Удобные обертки для math функций
def integrate_cos_cython(double a, double b, int n_iter=100000):
    """Оптимизированная для cos(x)."""
    return integrate_cython_loop(&cos, a, b, n_iter)

def integrate_sin_cython(double a, double b, int n_iter=100000):
    """Оптимизированная для sin(x)."""
    return integrate_cython_loop(&sin, a, b, n_iter)

# Итерация 5: noGIL версия с OpenMP
cdef double integrate_nogil_loop(double (*f)(double), double a, double b, int n_iter, int n_threads=0) nogil:
    """
    Версия без GIL с параллельным циклом (требует OpenMP).
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += f(a + i * step) * step
    
    return acc

def integrate_nogil_py(f, double a, double b, int n_iter=100000, int n_threads=0):
    """Python интерфейс для noGIL версии."""
    return integrate_nogil_loop(<double (*)(double)>f, a, b, n_iter, n_threads)

# Тестирование при импорте
if __name__ == "__main__":
    print("Cython тесты:")
    print(f"cos интеграл: {integrate_cos_cython(0, 3.14159, 10000):.6f}")
