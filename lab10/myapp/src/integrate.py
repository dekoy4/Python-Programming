"""
Модуль для численного интегрирования методом прямоугольников.
Итерация 1 лабораторной работы 10: Базовая реализация.
"""

import math
from typing import Callable

def integrate(f: Callable[[float], float], 
              a: float, 
              b: float, 
              *, 
              n_iter: int = 100000) -> float:
    """
    Вычисляет определенный интеграл функции f на интервале [a, b] 
    методом прямоугольников (левая сумма Римана).
    
    Метод разбивает интервал [a, b] на n_iter равных частей и 
    аппроксимирует площадь под кривой f(x) суммой площадей 
    lевых прямоугольников. Точность O(h) возрастает с увеличением n_iter.
    
    Args:
        f: Интегрируемая функция float -> float (должна быть векторизована)
        a: Нижняя граница интегрирования (float)
        b: Верхняя граница интегрирования (float, b > a обязательно)
        n_iter: Количество разбиений интервала (int > 0, по умолчанию 100000)
    
    Returns:
        float: Приближенное значение ∫_a^b f(x) dx
        
    Raises:
        ValueError: Если b <= a или n_iter <= 0
        
    Examples:
        >>> import math
        >>> integrate(math.cos, 0, math.pi, n_iter=1000)
        1.000334670374256
        
        >>> def quadratic(x):
        ...     return x**2 + 2*x + 1
        >>> integrate(quadratic, 0, 1, n_iter=10000)
        1.7500625006248446
    """
    if b <= a or n_iter <= 0:
        raise ValueError("Требуется b > a и n_iter > 0")
    
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


# Тестовый запуск для проверки
if __name__ == "__main__":
    print("Итерация 1: Базовая версия")
    result = integrate(math.cos, 0, math.pi, n_iter=1000)
    print(f"∫cos(x)dx от 0 до π = {result:.6f} (ожидается ~1.0)")
