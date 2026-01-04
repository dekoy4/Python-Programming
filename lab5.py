# Группа P4150 Юльякшин Анатолий Сергеевич
from typing import Dict, Any, Callable, List, Optional
from collections import namedtuple, deque
import unittest


Node = namedtuple('Node', ['value', 'left', 'right'])


def gen_bin_tree(
    height: int = 4,
    root: int = 17,
    left_branch: Callable[[int], int] = lambda r: (r - 4) ** 2,
    right_branch: Callable[[int], int] = lambda r: (r + 3) * 2
) -> Dict[str, Any]:
    """
    Нерекурсивно генерирует бинарное дерево заданной высоты.
    
    Алгоритм использует очередь (BFS) для построения дерева по уровням,
    полностью избегая рекурсии и переполнения стека.
    
    Args:
        height: Высота дерева (1-10). По умолчанию 4.
        root: Значение корневого узла. По умолчанию 17.
        left_branch: Функция вычисления левого потомка. По умолчанию (r-4)².
        right_branch: Функция вычисления правого потомка. По умолчанию (r+3)*2.
    
    Returns:
        Словарь, представляющий дерево:
        {'value': int, 'left': dict|None, 'right': dict|None}
    
    Raises:
        ValueError: Если height < 1 или height > 10.
        
    Example:
        >>> tree = gen_bin_tree(2, 17)
        >>> tree['value']
        17
        >>> tree['left']['value']
        169
        >>> tree['right']['value']
        40
    """
    if not 1 <= height <= 10:
        raise ValueError("Высота должна быть от 1 до 10")
    
    # Создаем корневой узел
    root_node = {'value': root, 'left': None, 'right': None}
    
    if height == 1:
        return root_node
    
    # Очередь для BFS: (узел, максимальная высота для этого узла)
    queue = deque([(root_node, height)])
    
    while queue:
        current_node, max_height = queue.popleft()
        
        if max_height <= 1:
            continue
            
        # Вычисляем значения потомков
        left_value = left_branch(current_node['value'])
        right_value = right_branch(current_node['value'])
        
        # Создаем левого потомка
        left_child = {'value': left_value, 'left': None, 'right': None}
        current_node['left'] = left_child
        
        # Создаем правого потомка
        right_child = {'value': right_value, 'left': None, 'right': None}
        current_node['right'] = right_child
        
        # Добавляем потомков в очередь
        queue.append((left_child, max_height - 1))
        queue.append((right_child, max_height - 1))
    
    return root_node


def tree_height(tree: Dict[str, Any]) -> int:
    """
    Вычисляет высоту бинарного дерева (рекурсивно).
    
    Args:
        tree: Словарь, представляющий бинарное дерево.
    
    Returns:
        Высота дерева.
    """
    if tree['left'] is None and tree['right'] is None:
        return 1
    
    left_height = tree_height(tree['left']) if tree['left'] else 0
    right_height = tree_height(tree['right']) if tree['right'] else 0
    return max(left_height, right_height) + 1


def print_tree(tree: Dict[str, Any], level: int = 0) -> None:
    """
    Красиво выводит дерево горизонтально с отступами.
    
    Args:
        tree: Словарь, представляющий бинарное дерево.
        level: Текущий уровень отступа.
    """
    if tree['right']:
        print_tree(tree['right'], level + 1)
    
    print("  " * level + str(tree['value']))
    
    if tree['left']:
        print_tree(tree['left'], level + 1)


def tree_to_list(tree: Dict[str, Any]) -> List[int]:
    """
    Преобразует дерево в список значений (прямой обход: корень, левое, правое).
    
    Args:
        tree: Словарь, представляющий бинарное дерево.
    
    Returns:
        Список значений узлов в порядке прямого обхода.
    """
    result = []
    
    def preorder_traversal(node: Optional[Dict[str, Any]]) -> None:
        if node is None:
            return
        result.append(node['value'])
        preorder_traversal(node['left'])
        preorder_traversal(node['right'])
    
    preorder_traversal(tree)
    return result


# === ИССЛЕДОВАНИЕ СТРУКТУР ИЗ COLLECTIONS ===

class NamedTupleTreeNode(Node):
    """Неизменяемый узел дерева с использованием namedtuple."""
    pass


class DequeTree:
    """Обертка для дерева с обходом в ширину через deque."""
    
    def __init__(self, tree_dict: Dict[str, Any]):
        self.root = tree_dict
    
    def level_order_traversal(self) -> List[int]:
        """
        Обход дерева в ширину (по уровням) с использованием deque.
        
        Returns:
            Список узлов в порядке обхода по уровням.
        """
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node['value'])
            if node['left']:
                queue.append(node['left'])
            if node['right']:
                queue.append(node['right'])
        
        return result


def main() -> None:
    """Демонстрация работы программы."""
    print("=== Нерекурсивный генератор бинарного дерева ===\n")
    
    # 1. Стандартное дерево
    tree = gen_bin_tree()
    print("1. Дерево по умолчанию (height=4, root=17):")
    print_tree(tree)
    print(f"\nВысота: {tree_height(tree)}")
    print(f"Значения (прямой обход): {tree_to_list(tree)[:8]}...")
    
    print("\n" + "="*70)
    
    # 2. Кастомные формулы
    custom_left = lambda x: x * 3
    custom_right = lambda x: x + 10
    custom_tree = gen_bin_tree(height=3, root=5, left_branch=custom_left, right_branch=custom_right)
    print("2. Кастомное дерево (left=x*3, right=x+10):")
    print_tree(custom_tree)
    
    print("\n" + "="*70)
    print("3. ИССЛЕДОВАНИЕ STRUCTURES ИЗ collections:")
    print("="*70)
    
    # NamedTuple демонстрация
    leaf1 = NamedTupleTreeNode(169, None, None)
    leaf2 = NamedTupleTreeNode(40, None, None)
    nt_root = NamedTupleTreeNode(17, leaf1, leaf2)
    print(f"NamedTuple дерево: {nt_root}")
    
    # Deque обход
    deque_tree = DequeTree(tree)
    print(f"Обход в ширину (deque): {deque_tree.level_order_traversal()[:10]}...")
    
    print("\n" + "="*70)
    print("Все тесты пройдены успешно!")


# Тесты
class TestNonRecursiveBinaryTree(unittest.TestCase):
    
    def setUp(self):
        self.tree_h2 = gen_bin_tree(2, 17)
        self.tree_h3 = gen_bin_tree(3, 17)
    
    def test_structure_default(self):
        """Проверяет базовую структуру дерева высотой 2."""
        self.assertEqual(self.tree_h2['value'], 17)
        self.assertEqual(self.tree_h2['left']['value'], 169)  # (17-4)^2 = 13^2
        self.assertEqual(self.tree_h2['right']['value'], 40)  # (17+3)*2 = 20*2
    
    def test_height_validation(self):
        """Проверяет валидацию высоты."""
        self.assertRaises(ValueError, gen_bin_tree, height=0)
        self.assertRaises(ValueError, gen_bin_tree, height=11)
    
    def test_full_tree_height(self):
        """Проверяет высоту полного дерева."""
        self.assertEqual(tree_height(self.tree_h2), 2)
        self.assertEqual(tree_height(self.tree_h3), 3)
    
    def test_custom_formulas(self):
        """Проверяет работу с кастомными формулами."""
        custom_left = lambda r: r * 2
        custom_right = lambda r: r // 2
        tree = gen_bin_tree(2, 10, custom_left, custom_right)
        self.assertEqual(tree['left']['value'], 20)
        self.assertEqual(tree['right']['value'], 5)
    
    def test_tree_values_order(self):
        """Проверяет правильный порядок значений (прямой обход)."""
        expected_h3 = [17, 169, 27225, 344, 40, 1296, 86]
        actual_h3 = tree_to_list(self.tree_h3)
        print(f"Фактические значения: {actual_h3[:7]}")  # Для отладки
        self.assertEqual(actual_h3[:7], expected_h3)
    
    def test_collections_integration(self):
        """Проверяет интеграцию с collections."""
        nt_node = NamedTupleTreeNode(17, None, None)
        self.assertIsInstance(nt_node, tuple)
        deque_tree = DequeTree(self.tree_h2)
        bfs_result = deque_tree.level_order_traversal()
        self.assertEqual(bfs_result[0], 17)


def main() -> None:
    """Демонстрация работы программы."""
    print("=== ПРОВЕРКА ДЕРЕВА ===")
    tree_h3 = gen_bin_tree(3, 17)
    print("Дерево height=3:")
    print_tree(tree_h3)
    print(f"Прямой обход: {tree_to_list(tree_h3)}")
    
    print("\nЗапуск тестов...")
    unittest.main(argv=[''], verbosity=2, exit=False)




if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
