"""
Итерации 2-3: Параллельное интегрирование с потоками и процессами.
Сравнение ThreadPoolExecutor vs ProcessPoolExecutor.
"""

import concurrent.futures as ftres
from functools import partial
from typing import Callable
from src.integrate import integrate

def integrate_threads(f: Callable[[float], float], 
                     a: float, 
                     b: float, 
                     *, 
                     n_jobs: int = 2, 
                     n_iter: int = 1000) -> float:
    """
    Вычисляет интеграл параллельно с помощью потоков (ThreadPoolExecutor).
    
    Разбивает интервал [a,b] на n_jobs частей и распределяет вычисления по потокам.
    
    Args:
        f: Интегрируемая функция
        a, b: Границы интегрирования (b > a)
        n_jobs: Количество потоков (по умолчанию 2)
        n_iter: Общее количество итераций (каждый поток получает n_iter//n_jobs)
    
    Returns:
        float: Значение интеграла
    
    Note:
        Из-за GIL потоки не дают ускорения для CPU-bound задач.
    """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    
    step = (b - a) / n_jobs
    partial_integrate = partial(integrate, f, n_iter=n_iter // n_jobs)
    
    futures = [
        executor.submit(partial_integrate, a + i * step, a + (i + 1) * step)
        for i in range(n_jobs)
    ]
    
    executor.shutdown()
    return sum(f.result() for f in futures)

def integrate_processes(f: Callable[[float], float], 
                       a: float, 
                       b: float, 
                       *, 
                       n_jobs: int = 2, 
                       n_iter: int = 1000) -> float:
    """
    Вычисляет интеграл параллельно с помощью процессов (ProcessPoolExecutor).
    
    Args:
        f: Интегрируемая функция
        a, b: Границы интегрирования
        n_jobs: Количество процессов (по умолчанию 2)
        n_iter: Общее количество итераций
    
    Returns:
        float: Значение интеграла
    
    Note:
        Процессы обходит GIL, обеспечивая настоящее параллельное выполнение.
    """
    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        partial_integrate = partial(integrate, f, n_iter=n_iter // n_jobs)
        
        futures = [
            executor.submit(partial_integrate, a + i * step, a + (i + 1) * step)
            for i in range(n_jobs)
        ]
        
        return sum(f.result() for f in ftres.as_completed(futures))

# Тестирование
if __name__ == "__main__":
    import math
    
    print("Итерация 2-3: Тестирование потоков и процессов")
    print("∫cos(x)dx от 0 до π")
    
    result_threads = integrate_threads(math.cos, 0, math.pi, n_jobs=4, n_iter=10000)
    print(f"Потоки (4): {result_threads:.6f}")
    
    result_processes = integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=10000)
    print(f"Процессы (4): {result_processes:.6f}")
    
    print("Ожидаемый результат: ~1.0")
