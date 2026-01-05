#cython: language_level=3, boundscheck=False, wraparound=False

cdef extern from "math.h":
    double cos(double)

def integrate_cos_cython(double a, double b, int n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += cos(a + i * step) * step
    return acc

def integrate_python(f, double a, double b, int n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc
