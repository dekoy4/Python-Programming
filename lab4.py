# Группа P4150 Юльякшин Анатолий Сергеевич
from typing import List
import timeit
import matplotlib.pyplot as plt
import numpy as np
from functools import lru_cache
import unittest


def fact_recursive(n: int) -> int:
    """
    Рекурсивный алгоритм вычисления факториала.
    
    Сложность: O(n) по времени, O(n) по памяти (из-за рекурсии).
    
    Args:
        n: неотрицательное целое число
        
    Returns:
        Факториал числа n (n!)
        
    Raises:
        ValueError: если n < 0
        
    Example:
        >>> fact_recursive(5)
        120
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    if n <= 1:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """
    Итеративный алгоритм вычисления факториала (через цикл).
    
    Сложность: O(n) по времени, O(1) по памяти.
    
    Args:
        n: неотрицательное целое число
        
    Returns:
        Факториал числа n (n!)
        
    Raises:
        ValueError: если n < 0
        
    Example:
        >>> fact_iterative(5)
        120
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def benchmark_factorials(
    test_values: List[int], 
    number: int = 1000
) -> tuple[List[float], List[float], List[int]]:
    """
    Бенчмарк сравнения двух реализаций факториала.
    
    Args:
        test_values: список чисел для тестирования
        number: количество повторений для timeit
        
    Returns:
        Кортеж (времена рекурсии, времена итерации, тест. значения)
    """
    recursive_times = []
    iterative_times = []
    
    print("Выполнение бенчмарка...")
    for n in test_values:
        # Измеряем время одного вызова (среднее по number повторений)
        rec_time = timeit.timeit(lambda: fact_recursive(n), number=number) / number
        iter_time = timeit.timeit(lambda: fact_iterative(n), number=number) / number
        
        recursive_times.append(rec_time)
        iterative_times.append(iter_time)
        
        print(f"n={n:3d}: рекурсия={rec_time:.2e}с, итерация={iter_time:.2e}с")
    
    return recursive_times, iterative_times, test_values


def plot_comparison(
    test_values: List[int], 
    rec_times: List[float], 
    iter_times: List[float]
) -> None:
    """
    Строит график сравнения времени выполнения двух алгоритмов.
    
    Args:
        test_values: значения n для тестирования
        rec_times: времена выполнения рекурсивной версии
        iter_times: времена выполнения итеративной версии
    """
    plt.figure(figsize=(12, 8))
    
    plt.plot(test_values, rec_times, 'ro-', linewidth=2, markersize=8, 
             label='Рекурсивная реализация', alpha=0.8)
    plt.plot(test_values, iter_times, 'bs-', linewidth=2, markersize=8, 
             label='Итеративная реализация', alpha=0.8)
    
    plt.xlabel('n (размер входных данных)', fontsize=12)
    plt.ylabel('Время выполнения (сек)', fontsize=12)
    plt.title('Сравнение времени вычисления факториала\n(среднее время одного вызова)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Логарифмическая шкала для Y для лучшей видимости
    
    # Добавляем таблицу соотношения скоростей
    speedup = [r/i if i > 0 else 0 for r, i in zip(rec_times, iter_times)]
    plt.text(0.02, 0.98, f'Ускорение итерации:\nмакс. x{max_speedup:=.1f}', 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Главная функция для запуска бенчмарка и визуализации."""
    # Фиксированный список для тестирования (до разумных пределов рекурсии)
    test_values = list(range(5, 26, 2))  # [5,7,9,...,25]
    
    print("=== Сравнение реализаций факториала ===\n")
    
    # Проводим бенчмарк
    rec_times, iter_times, values = benchmark_factorials(test_values, number=10000)
    
    # Вычисляем ускорение
    global max_speedup
    speedup = [r/i if i > 0 else 0 for r, i in zip(rec_times, iter_times)]
    max_speedup = max(speedup)
    
    print(f"\nМаксимальное ускорение итеративной версии: x{max_speedup:.1f}")
    
    # Строим график
    plot_comparison(values, rec_times, iter_times)


if __name__ == "__main__":
    main()

# Тесты
class TestFactorial(unittest.TestCase):
    
    def test_correctness(self):
        """Проверка корректности вычислений."""
        test_cases = [(0, 1), (1, 1), (5, 120), (10, 3628800)]
        
        for n, expected in test_cases:
            self.assertEqual(fact_recursive(n), expected)
            self.assertEqual(fact_iterative(n), expected)
    
    def test_negative_input(self):
        """Проверка обработки отрицательных чисел."""
        self.assertRaises(ValueError, fact_recursive, -1)
        self.assertRaises(ValueError, fact_iterative, -1)
    
    def test_performance_trend(self):
        """Проверка, что итеративная версия быстрее."""
        n = 15
        rec_time = timeit.timeit(lambda: fact_recursive(n), number=1000) / 1000
        iter_time = timeit.timeit(lambda: fact_iterative(n), number=1000) / 1000
        self.assertLess(iter_time, rec_time, 
                       "Итеративная версия должна быть быстрее")


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
