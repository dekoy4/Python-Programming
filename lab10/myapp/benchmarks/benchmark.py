"""
Итерация 1: Замеры производительности базовой функции integrate().
Сравнение времени выполнения для различного числа итераций.
"""

import timeit
import math
import sys
import csv
from pathlib import Path
from typing import Dict, Any
import gc

# Импортируем тестируемую функцию
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from integrate import integrate

RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def benchmark_integrate(n_iters: list[int], repeats: int = 20) -> Dict[str, list[float]]:
    """
    Замеряет время выполнения функции integrate для разных n_iter.
    
    Args:
        n_iters: Список значений n_iter для тестирования
        repeats: Количество повторений каждого замера
    
    Returns:
        Словарь {n_iter: среднее_время_сек}
    """
    print("Замеры производительности базовой функции integrate()")
    print(f"{'n_iter':>8} | {'Время (сек)':>12} | {'±σ (сек)':>10}")
    print("-" * 35)
    
    timings = {}
    
    for n_iter in n_iters:
        # Функция для замера (lambda для timeit)
        test_func = lambda: integrate(math.cos, 0, math.pi, n_iter=n_iter)
        
        # Очистка GC и разогрев
        gc.disable()
        for _ in range(3):  # warmup
            test_func()
        gc.enable()
        
        # Основной замер
        times = timeit.repeat(
            test_func,
            number=1,  # 1 вызов функции за итерацию
            repeat=repeats,
            globals=globals()
        )
        
        avg_time = sum(times) / len(times)
        std_time = (sum((x - avg_time) ** 2 for x in times) / len(times)) ** 0.5
        
        timings[n_iter] = avg_time
        
        print(f"{n_iter:8d} | {avg_time:12.4f} | {std_time:10.4f}")
    
    return timings

def save_results(timings: Dict[int, float], filename: str = "timings.csv"):
    """Сохраняет результаты в CSV."""
    filepath = RESULTS_DIR / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['n_iter', 'time_sec', 'method'])
        for n_iter, time_sec in timings.items():
            writer.writerow([n_iter, f"{time_sec:.6f}", "baseline_python"])
    
    print(f"Результаты сохранены: {filepath}")

def print_summary(timings: Dict[int, float]):
    """Печатает краткую сводку."""
    print("\nСВОДКА (Итерация 1):")
    print(f"  n_iter=100000: {timings.get(100000, 'N/A'):>8.2f} сек")
    print(f"  Ускорение: 1.0x (базовый уровень)")

if __name__ == "__main__":
    # Наборы для тестирования (Итерация 1)
    N_ITERS = [1000, 10000, 100000]
    
    timings = benchmark_integrate(N_ITERS)
    save_results(timings)
    print_summary(timings)
