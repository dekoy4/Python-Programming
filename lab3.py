# Группа P4150 Юльякшин Анатолий Сергеевич
from typing import Dict, Any, Union, Optional, List, Tuple
from collections import namedtuple, deque
import unittest


Node = namedtuple('Node', ['value', 'left', 'right'])


def gen_bin_tree(height: int = 4, root: int = 17) -> Dict[str, Any]:
    """
    Рекурсивно генерирует бинарное дерево заданной высоты с корнем root.
    
    Формулы для потомков:
    - left_leaf = (parent - 4)²
    - right_leaf = (parent + 3) * 2
    
    Args:
        height: Высота дерева (1-10). По умолчанию 4.
        root: Значение корневого узла. По умолчанию 17.
    
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
    """
    if not 1 <= height <= 10:
        raise ValueError("Высота должна быть от 1 до 10")
    
    if height == 1:
        return {'value': root, 'left': None, 'right': None}
    
    left_value = (root - 4) ** 2
    right_value = (root + 3) * 2
    
    left_child = gen_bin_tree(height - 1, left_value)
    right_child = gen_bin_tree(height - 1, right_value)
    
    return {
        'value': root,
        'left': left_child,
        'right': right_child
    }


def tree_to_list(tree: Dict[str, Any]) -> List[int]:
    """
    Преобразует дерево в список значений (прямой обход).
    
    Args:
        tree: Словарь, представляющий бинарное дерево.
    
    Returns:
        Список значений узлов в порядке прямого обхода.
    """
    result = []
    
    def traverse(node: Optional[Dict[str, Any]]) -> None:
        if node is None:
            return
        result.append(node['value'])
        traverse(node['left'])
        traverse(node['right'])
    
    traverse(tree)
    return result


def tree_height(tree: Dict[str, Any]) -> int:
    """
    Вычисляет высоту бинарного дерева.
    
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
    Выводит дерево в читаемом виде (горизонтально).
    
    Args:
        tree: Словарь, представляющий бинарное дерево.
        level: Текущий уровень для отступов.
    """
    if tree['left'] is None and tree['right'] is None:
        print("  " * level + str(tree['value']))
        return
    
    print_tree(tree['right'], level + 1) if tree['right'] else None
    print("  " * level + str(tree['value']))
    print_tree(tree['left'], level + 1) if tree['left'] else None


# Исследование альтернативных структур из collections
class NamedTupleTreeNode(Node):
    """Использование namedtuple для узлов дерева."""
    pass


class DequeTree:
    """Представление дерева с использованием deque для обхода."""
    
    def __init__(self, tree_dict: Dict[str, Any]):
        self.root = tree_dict
    
    def level_order_traversal(self) -> List[int]:
        """Обход в ширину с использованием deque."""
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
    print("=== Генератор бинарного дерева ===\n")
    
    # Стандартное дерево
    tree = gen_bin_tree(4, 17)
    print("Дерево высотой 4, корень=17:")
    print_tree(tree)
    print(f"\nВысота: {tree_height(tree)}")
    print(f"Значения (прямой обход): {tree_to_list(tree)[:10]}...")
    
    print("\n" + "="*50)
    print("Исследование структур collections:")
    print("="*50)
    
    # NamedTuple представление
    root_node = NamedTupleTreeNode(
        value=17,
        left=NamedTupleTreeNode(value=169, left=None, right=None),
        right=NamedTupleTreeNode(value=40, left=None, right=None)
    )
    print(f"NamedTuple узел: {root_node}")
    
    # Deque обход
    deque_tree = DequeTree(tree)
    print(f"Обход в ширину (deque): {deque_tree.level_order_traversal()[:8]}...")


if __name__ == "__main__":
    main()

# Тесты
class TestBinaryTree(unittest.TestCase):
    
    def setUp(self):
        """Создание тестового дерева высотой 2."""
        self.tree = gen_bin_tree(height=2, root=17)
    
    def test_gen_bin_tree_structure(self):
        """Проверка структуры дерева высотой 2."""
        self.assertEqual(self.tree['value'], 17)
        self.assertIsNotNone(self.tree['left'])
        self.assertIsNotNone(self.tree['right'])
        self.assertEqual(self.tree['left']['value'], (17 - 4) ** 2)  # 169
        self.assertEqual(self.tree['right']['value'], (17 + 3) * 2)  # 40
    
    def test_tree_height(self):
        """Проверка вычисления высоты."""
        self.assertEqual(tree_height(self.tree), 2)
        full_tree = gen_bin_tree(4, 17)
        self.assertEqual(tree_height(full_tree), 4)
    
    def test_tree_values(self):
        """Проверка значений узлов."""
        values = tree_to_list(self.tree)
        expected = [17, 169, 40]
        self.assertEqual(values, expected)
    
    def test_edge_cases(self):
        """Тест граничных случаев."""
        # Высота 1
        leaf = gen_bin_tree(1, 100)
        self.assertEqual(leaf['value'], 100)
        self.assertIsNone(leaf['left'])
        self.assertIsNone(leaf['right'])
        
        # Максимальная высота
        deep_tree = gen_bin_tree(10, 17)
        self.assertEqual(tree_height(deep_tree), 10)
    
    def test_invalid_height(self):
        """Тест некорректных параметров."""
        self.assertRaises(ValueError, gen_bin_tree, 0)
        self.assertRaises(ValueError, gen_bin_tree, 11)
    
    def test_collections_integration(self):
        """Тест интеграции с collections."""
        deque_tree = DequeTree(self.tree)
        level_order = deque_tree.level_order_traversal()
        self.assertEqual(level_order[0], 17)  # Корень первый


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False) # вместо unittest.main()
