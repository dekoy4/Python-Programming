"""
Процессы с большим n_iter (реалистичный тест)
"""
import timeit
import math
import sys
from pathlib import Path
from multiprocessing import freeze_support

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.integrate_async import integrate_processes

if __name__ == '__main__':
    freeze_support()
    
    # ТЕСТИРУЕМ 3 СЦЕНАРИЯ:
    for n_iter in [500000, 1000000, 2000000]:
        print(f"\nn_iter={n_iter:,}")
        print("-" * 40)
        
        # Python
        t_python = timeit.timeit(
            lambda: integrate(math.cos, 0, math.pi, n_iter=n_iter), 
            number=3
        ) / 3 * 1000
        
        # Процессы
        t_processes = timeit.timeit(
            lambda: integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=n_iter), 
            number=3
        ) / 3 * 1000
        
        speedup = t_python / t_processes
        print(f"Python:    {t_python:6.1f}мс")
        print(f"Процессы:  {t_processes:6.1f}мс ({speedup:.1f}x)")
