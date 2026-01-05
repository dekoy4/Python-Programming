"""
Тест процессов отдельно (исправленная версия)
"""
import timeit
import math
import sys
from pathlib import Path
from multiprocessing import freeze_support

# ФИКС импорта
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.integrate_async import integrate_processes

if __name__ == '__main__':
    freeze_support()
    print("Процессы (n_jobs=4, n_iter=100000):")
    t = timeit.timeit(
        lambda: integrate_processes(math.cos, 0, math.pi, n_jobs=4, n_iter=100000), 
        number=3
    ) / 3 * 1000  # 3 повторения, в миллисекунды
    print(f"Processes(4): {t:.1f}мс (~{10.3/t:.1f}x к Python)")
