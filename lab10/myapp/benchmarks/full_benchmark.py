import timeit, math
from src import integrate, integrate_threads, integrate_processes

methods = {
    "Python": lambda: integrate(math.cos, 0, math.pi, n_iter=100000),
    "Threads(4)": lambda: integrate_threads(math.cos, 0, math.pi, n_jobs=4, n_iter=100000),
    "Processes(4)": lambda: integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=100000),
}

print("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ (n=100k)")
for name, func in methods.items():
    t = timeit.timeit(func, number=10) / 10 * 1000
    speedup = 0.07 / (t/1000)  # относительно Python
    print(f"{name:12} | {t:6.1f}ms | {speedup:4.1f}x")
