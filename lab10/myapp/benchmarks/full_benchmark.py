"""
Полный бенчмарк лабораторной
"""
import timeit
import math
from multiprocessing import freeze_support
import sys
from pathlib import Path

# КРИТИЧНО: sys.path ДО импортов
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.integrate import integrate
from src.integrate_async import integrate_threads

def benchmark_methods():
    """Запуск бенчмарка БЕЗ multiprocessing проблем"""
    methods = {
        "Python": lambda: integrate(math.cos, 0, math.pi, n_iter=100000),
        "Threads(4)": lambda: integrate_threads(math.cos, 0, math.pi, n_jobs=4, n_iter=100000),
    }
    
    print("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ 10 (n_iter=100000)")
    print("Метод          | Время (мс) | Ускорение")
    print("-" * 40)
    
    baseline_time = None
    for name, func in methods.items():
        total_time = timeit.timeit(func, number=5)  # Уменьшено до 5
        avg_time_ms = (total_time / 5) * 1000
        
        if name == "Python":
            baseline_time = avg_time_ms
        
        speedup = baseline_time / avg_time_ms if baseline_time else 1.0
        print(f"{name:<12} | {avg_time_ms:8.1f}мс | {speedup:6.1f}x")
    
    print("\n✓ Бенчмарк завершен успешно!")
    print("Вывод: Потоки медленнее Python из-за GIL")

if __name__ == '__main__':
    freeze_support()  # ФИКС multiprocessing для Windows
    benchmark_methods()
