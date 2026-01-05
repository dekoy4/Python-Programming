from src.integrate_async import integrate_processes
import timeit, math

if __name__ == '__main__':
    print("Процессы (отдельно):")
    t = timeit.timeit(lambda: integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=100000), number=3) / 3 * 1000
    print(f"Processes(4): {t:.1f}мс")
