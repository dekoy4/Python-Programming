#cython: language_level=3

cdef extern from "math.h":
    double cos(double x)

def integrate_cos(double a, double b, int n):
    cdef double sum = 0.0
    cdef double h = (b - a) / n
    cdef int i
    for i in range(n):
        sum += cos(a + i * h) * h
    return sum
