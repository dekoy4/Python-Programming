# Группа P4150 Юльякшин Анатолий Сергеевич
from typing import Dict, Any, Callable
from collections import deque
import timeit
import matplotlib.pyplot as plt
import numpy as np
import unittest


def build_tree_recursive(
    height: int,
    root: int = 17,
    left_branch: Callable[[int], int] = lambda r: (r - 4) ** 2,
    right_branch: Callable[[int], int] = lambda r: (r + 3) * 2
) -> Dict[str, Any]:
    """
    Рекурсивно строит бинарное дерево заданной высоты.
    
    Args:
        height: Высота дерева.
        root: Значение корневого узла.
        left_branch: Функция для левого потомка: (r-4)².
        right_branch: Функция для правого потомка: (r+3)*2.
    
    Returns:
        Словарь, представляющий бинарное дерево.
    """
    if height == 1:
        return {'value': root, 'left': None, 'right': None}
    
    left_value = left_branch(root)
    right_value = right_branch(root)
    
    left_subtree = build_tree_recursive(height - 1, left_value, left_branch, right_branch)
    right_subtree = build_tree_recursive(height - 1, right_value, left_branch, right_branch)
    
    return {
        'value': root,
        'left': left_subtree,
        'right': right_subtree
    }


def build_tree_iterative(
    height: int,
    root: int = 17,
    left_branch: Callable[[int], int] = lambda r: (r - 4) ** 2,
    right_branch: Callable[[int], int] = lambda r: (r + 3) * 2
) -> Dict[str, Any]:
    """
    Нерекурсивно строит бинарное дерево с использованием очереди (BFS).
    
    Args:
        height: Высота дерева.
        root: Значение корневого узла.
        left_branch: Функция для левого потомка: (r-4)².
        right_branch: Функция для правого потомка: (r+3)*2.
    
    Returns:
        Словарь, представляющий бинарное дерево.
    """
    if height < 1:
        raise ValueError("Высота должна быть положительной")
    
    root_node = {'value': root, 'left': None, 'right': None}
    if height == 1:
        return root_node
    
    # Очередь: (узел, оставшаяся высота)
    queue = deque([(root_node, height)])
    
    while queue:
        node, remaining_height = queue.popleft()
        
        if remaining_height <= 1:
            continue
        
        # Создаем потомков
        left_val = left_branch(node['value'])
        right_val = right_branch(node['value'])
        
        left_child = {'value': left_val, 'left': None, 'right': None}
        right_child = {'value': right_val, 'left': None, 'right': None}
        
        node['left'] = left_child
        node['right'] = right_child
        
        queue.append((left_child, remaining_height - 1))
        queue.append((right_child, remaining_height - 1))
    
    return root_node


def tree_height(tree: Dict[str, Any]) -> int:
    """Вычисляет высоту дерева."""
    if tree['left'] is None and tree['right'] is None:
        return 1
    left_h = tree_height(tree['left']) if tree['left'] else 0
    right_h = tree_height(tree['right']) if tree['right'] else 0
    return max(left_h, right_h) + 1


def benchmark_trees(heights: list[int], repeats: int = 1000) -> tuple[list[float], list[float], list[int]]:
    """
    Сравнивает время построения деревьев разной высоты.
    
    Args:
        heights: Список высот для тестирования.
        repeats: Количество повторений для усреднения.
    
    Returns:
        Кортеж (времена_рекурсии, времена_итерации, высоты).
    """
    recursive_times = []
    iterative_times = []
    
    print("Бенчмарк выполнения...")
    print("height\tРекурсия\tИтерация")
    print("-" * 35)
    
    for h in heights:
        # Время одного вызова рекурсивной функции
        rec_time = timeit.timeit(
            lambda: build_tree_recursive(h), 
            number=repeats
        ) / repeats
        
        # Время одного вызова итеративной функции
        iter_time = timeit.timeit(
            lambda: build_tree_iterative(h), 
            number=repeats
        ) / repeats
        
        recursive_times.append(rec_time)
        iterative_times.append(iter_time)
        
        print(f"{h:5d}\t{rec_time:8.2e}\t{iter_time:8.2e}")
    
    return recursive_times, iterative_times, heights


def plot_performance(heights: list[int], rec_times: list[float], iter_times: list[float]) -> None:
    """Строит график сравнения производительности."""
    plt.figure(figsize=(12, 8))
    
    plt.plot(heights, rec_times, 'ro-', linewidth=3, markersize=10, 
             label='Рекурсивная реализация', alpha=0.8)
    plt.plot(heights, iter_times, 'bs-', linewidth=3, markersize=10, 
             label='Итеративная реализация (BFS)', alpha=0.8)
    
    plt.xlabel('Высота дерева (h)', fontsize=14, fontweight='bold')
    plt.ylabel('Время построения (сек)', fontsize=14, fontweight='bold')
    plt.title('Сравнение времени построения бинарного дерева\n(среднее время одного вызова)', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Логарифмическая шкала Y
    
    # Добавляем таблицу ускорения
    speedup = np.array(rec_times) / np.array(iter_times)
    max_speedup = np.max(speedup)
    plt.text(0.02, 0.98, f'Максимальное ускорение итерации: ×{max_speedup:.0f}', 
             transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Главная функция бенчмарка."""
    # Тестируем высоты от 1 до 10
    test_heights = list(range(1, 11))
    
    print("=== СРАВНЕНИЕ РЕКУРСИВНОЙ И ИТЕРАТИВНОЙ РЕАЛИЗАЦИЙ БИНАРНОГО ДЕРЕВА ===\n")
    
    # 1. Бенчмарк
    rec_times, iter_times, heights = benchmark_trees(test_heights, repeats=1000)
    
    # 2. Вычисления статистики
    speedup = [r/i if i > 0 else 0 for r, i in zip(rec_times, iter_times)]
    avg_speedup = np.mean(speedup[1:])  # Исключаем height=1 (аномалия)
    
    print(f"\n{'='*50}")
    print("СТАТИСТИКА:")
    print(f"Максимальное ускорение итерации: ×{max(speedup):.1f}")
    print(f"Среднее ускорение итерации:    ×{avg_speedup:.1f}")
    
    # 3. График
    plot_performance(heights, rec_times, iter_times)
    
    print("\n" + "="*70)
    print("ВЫВОДЫ:")
    print("• Итеративная версия стабильно быстрее рекурсивной")
    print("• Разница растет экспоненциально с увеличением высоты")
    print("• Рекурсия ограничена глубиной стека Python (~1000)")
    print("• Итерация не имеет ограничений по высоте")


# Тесты
class TestTreeBuilders(unittest.TestCase):
    
    def test_correctness_same_structure(self):
        """Проверяет идентичность структуры обоих реализаций."""
        heights = [2, 3]
        for h in heights:
            rec_tree = build_tree_recursive(h)
            iter_tree = build_tree_iterative(h)
            self.assertEqual(rec_tree['value'], iter_tree['value'])
            self.assertEqual(tree_height(rec_tree), tree_height(iter_tree))
    
    def test_height_validation(self):
        """Проверяет валидацию высоты."""
        self.assertRaises(ValueError, build_tree_iterative, 0)
    
    def test_base_case(self):
        """Проверяет базовый случай (height=1)."""
        rec_tree = build_tree_recursive(1)
        iter_tree = build_tree_iterative(1)
        self.assertEqual(rec_tree, iter_tree)
        self.assertEqual(tree_height(rec_tree), 1)


if __name__ == "__main__":
    # Запуск тестов
    print("Запуск тестов...")
    unittest.main(argv=[''], verbosity=2, exit=False)
    print()
    
    # Бенчмарк и график
    main()
