"""
Юнит-тесты для модуля интегрирования (Итерация 1).
Покрывает: точность вычислений, устойчивость к n_iter, граничные случаи.
"""

import unittest
import math
import doctest
from unittest.mock import patch
from src.integrate import integrate

class TestIntegrate(unittest.TestCase):
    
    def test_cos_integral_known_value(self):
        """∫cos(x)dx от 0 до π = sin(π) - sin(0) = 0 точно"""
        result = integrate(math.cos, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result, 0.0, places=3, msg="Интеграл cos(x) должен быть 0")
    
    def test_quadratic_integral_known_value(self):
        """∫x²dx от 0 до 1 = [x³/3] от 0 до 1 = 1/3 ≈ 0.33333"""
        def quadratic(x): 
            return x * x
        result = integrate(quadratic, 0, 1, n_iter=10000)
        self.assertAlmostEqual(result, 1/3, places=3, msg="Интеграл x² от 0 до 1 = 1/3")
    
    def test_n_iter_stability(self):
        """Проверка сходимости при разном n_iter (должна стабилизироваться)"""
        def quadratic(x): 
            return x * x
        
        result_1k = integrate(quadratic, 0, 1, n_iter=1000)
        result_10k = integrate(quadratic, 0, 1, n_iter=10000)
        result_100k = integrate(quadratic, 0, 1, n_iter=100000)
        
        self.assertAlmostEqual(result_10k, result_100k, places=4, 
                             msg="Высокое n_iter должно давать стабильный результат")
        self.assertAlmostEqual(result_1k, result_10k, places=2,
                             msg="Увеличение n_iter улучшает точность")
    
    def test_invalid_bounds_a_gt_b(self):
        """Проверка ошибки при a > b"""
        with self.assertRaises(ValueError, msg="Должна быть ошибка при a > b"):
            integrate(math.cos, 1, 0, n_iter=1000)
    
    def test_invalid_n_iter_negative(self):
        """Проверка ошибки при n_iter <= 0"""
        with self.assertRaises(ValueError, msg="n_iter должен быть > 0"):
            integrate(math.cos, 0, 1, n_iter=-1)
    
    def test_invalid_n_iter_zero(self):
        """Проверка ошибки при n_iter = 0"""
        with self.assertRaises(ValueError, msg="n_iter = 0 недопустим"):
            integrate(math.cos, 0, 1, n_iter=0)
    
    def test_function_with_constant(self):
        """∫1dx от 0 до 5 = 5 (постоянная функция)"""
        def constant(x):
            return 1.0
        result = integrate(constant, 0, 5, n_iter=5000)
        self.assertAlmostEqual(result, 5.0, places=3)

def test_doctests():
    """Запуск doctest из модуля integrate."""
    import sys
    import doctest
    sys.path.insert(0, '..')
    import src.integrate
    return doctest.testmod(src.integrate)

if __name__ == "__main__":
    # Запуск unittest
    print("Запуск юнит-тестов...")
    unittest.main(verbosity=2, exit=False)
    
    # Запуск doctest
    print("\nЗапуск doctest...")
    doctest_result = test_doctests()
    print(f"Doctest: {doctest_result[0]} тестов пройдено успешно")
