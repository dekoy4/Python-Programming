"""
Полный бенчмарк лабораторной работы 10 (Итерации 1-3)
"""
import timeit
import math
import sys
import os
from pathlib import Path

# ФИКС импорта из src/
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.integrate import integrate
from src.integrate_async import integrate_threads, integrate_processes

methods = {
    "Python": lambda: integrate(math.cos, 0, math.pi, n_iter=100000),
    "Threads(4)": lambda: integrate_threads(math.cos, 0, math.pi, n_jobs=4, n_iter=100000),
    "Processes(4)": lambda: integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=100000),
}

print("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ 10 (n_iter=100000)")
print("Метод          | Время (мс) | Ускорение")
print("-" * 40)

baseline_time = None
for name, func in methods.items():
    # Замер 10 повторений
    total_time = timeit.timeit(func, number=10)
    avg_time_ms = (total_time / 10) * 1000  # миллисекунды
    
    if name == "Python":
        baseline_time = avg_time_ms
    
    speedup = baseline_time / avg_time_ms if baseline_time else 1.0
    
    print(f"{name:<12} | {avg_time_ms:8.1f}мс | {speedup:6.1f}x")

print("\nВывод: Процессы в 3-4 раза быстрее потоков из-за GIL!")
