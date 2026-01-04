from typing import List, Tuple, Callable
import random
import unittest


def generate_search_list(start: int, end: int) -> List[int]:
    """
    Генерирует список чисел в заданном диапазоне для поиска.

    Args:
        start: Начало диапазона (включительно).
        end: Конец диапазона (включительно).

    Returns:
        Список чисел от start до end включительно.

    Raises:
        ValueError: Если start > end.

    Example:
        >>> generate_search_list(1, 5)
        [1, 2, 3, 4, 5]
    """
    if start > end:
        raise ValueError("Начало диапазона не может быть больше конца")
    return list(range(start, end + 1))


def get_user_range() -> Tuple[int, int]:
    """
    Получает диапазон поиска с клавиатуры.

    Returns:
        Кортеж (начало, конец) диапазона.

    Raises:
        ValueError: При некорректном вводе.
    """
    try:
        start = int(input("Введите начало диапазона: "))
        end = int(input("Введите конец диапазона: "))
        return start, end
    except ValueError:
        raise ValueError("Введите целые числа")


def linear_search_guesser(target: int, search_list: List[int]) -> int:
    """
    Медленный перебор (линейный поиск) по списку.

    Args:
        target: Целевое число.
        search_list: Список для поиска.

    Returns:
        Количество попыток.
    """
    for i, num in enumerate(search_list, 1):
        if num == target:
            return i
    raise ValueError("Число не найдено в списке")


def binary_search_guesser(target: int, search_list: List[int]) -> int:
    """
    Бинарный поиск в отсортированном списке.

    Args:
        target: Целевое число.
        search_list: Отсортированный список для поиска.

    Returns:
        Количество попыток.

    Raises:
        ValueError: Если список не отсортирован или число не найдено.
    """
    if search_list != sorted(search_list):
        raise ValueError("Список должен быть отсортирован для бинарного поиска")
    
    left, right = 0, len(search_list) - 1
    attempts = 0
    
    while left <= right:
        attempts += 1
        mid = (left + right) // 2
        
        if search_list[mid] == target:
            return attempts
        elif search_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    raise ValueError("Число не найдено в списке")


def guess_number(
    target: int, 
    search_list: List[int], 
    method: str = 'linear'
) -> Tuple[int, int]:
    """
    Основная функция игры "угадай число".

    Args:
        target: Загаданное число.
        search_list: Список чисел для поиска (не должен содержать target).
        method: Метод поиска ('linear' или 'binary').

    Returns:
        Кортеж (найденное число, количество попыток).

    Raises:
        ValueError: При неверном методе или числе вне списка.
    """
    methods: dict[str, Callable[[int, List[int]], int]] = {
        'linear': linear_search_guesser,
        'binary': binary_search_guesser
    }
    
    if method not in methods:
        raise ValueError("Метод должен быть 'linear' или 'binary'")
    
    if target not in search_list:
        raise ValueError(f"Число {target} отсутствует в списке")
    
    attempts = methods[method](target, search_list)
    return target, attempts


def play_game() -> None:
    """
    Интерактивная игра с вводом от пользователя.
    """
    try:
        print("=== Игра 'Угадай число' ===")
        start, end = get_user_range()
        search_list = generate_search_list(start, end)
        
        target = random.choice(search_list)
        print(f"\nЯ загадал число от {start} до {end}. Угадайте!")
        
        print("\nВыберите метод:")
        print("1 - Медленный перебор")
        print("2 - Бинарный поиск")
        
        choice = input("Ваш выбор (1 или 2): ")
        method = 'linear' if choice == '1' else 'binary'
        
        result = guess_number(target, search_list, method)
        print(f"\nУгадано число {result[0]} за {result[1]} попыток!")
        
    except ValueError as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\nИгра прервана.")


if __name__ == "__main__":
    play_game()

# Тесты

class TestGuessNumber(unittest.TestCase):
    
    def test_generate_search_list(self):
        """Тест генерации списка."""
        self.assertEqual(generate_search_list(1, 5), [1, 2, 3, 4, 5])
        self.assertEqual(generate_search_list(0, 0), [0])
        self.assertRaises(ValueError, generate_search_list, 5, 1)
    
    def test_linear_search(self):
        """Тест линейного поиска."""
        search_list = [1, 3, 5, 7, 9]
        result = guess_number(5, search_list, 'linear')
        self.assertEqual(result, (5, 3))
        
        result = guess_number(1, search_list, 'linear')
        self.assertEqual(result, (1, 1))
    
    def test_binary_search(self):
        """Тест бинарного поиска."""
        search_list = [1, 3, 5, 7, 9]
        result = guess_number(5, search_list, 'binary')
        self.assertEqual(result[0], 5)
        self.assertLessEqual(result[1], 3)  # Бинарный поиск эффективнее
        
        # Тест на неотсортированный список
        unsorted = [5, 1, 3, 9, 7]
        self.assertRaises(ValueError, guess_number, 5, unsorted, 'binary')
    
    def test_errors(self):
        """Тест обработки ошибок."""
        search_list = [1, 2, 3]
        
        # Неверный метод
        self.assertRaises(ValueError, guess_number, 2, search_list, 'invalid')
        
        # Число вне списка
        self.assertRaises(ValueError, guess_number, 99, search_list, 'linear')
    
    def test_edge_cases(self):
        """Тест граничных случаев."""
        # Одно число
        lst = [42]
        result = guess_number(42, lst, 'linear')
        self.assertEqual(result, (42, 1))
        
        # Последнее число
        lst = list(range(1, 101))
        result = guess_number(100, lst, 'linear')
        self.assertEqual(result, (100, 100))


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
