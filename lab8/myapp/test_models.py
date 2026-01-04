"""Тесты для моделей."""

import unittest
from models import Author, App, User, Currency, UserCurrency


class TestModels(unittest.TestCase):
    """Тестовый класс для моделей."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.author = Author("Иван Иванов", "ИТ-21")
        self.app = App("TestApp", "1.0", self.author)
        self.user = User("user1", "Алексей")
        self.currency = Currency(
            char_code="USD", value=90.1234, nominal=1
        )
    
    def test_author(self):
        """Тест модели Author."""
        self.assertEqual(self.author.name, "Иван Иванов")
        self.assertEqual(self.author.group, "ИТ-21")
    
    def test_app(self):
        """Тест модели App."""
        self.assertEqual(self.app.name, "TestApp")
        self.assertEqual(self.app.version, "1.0")
        self.assertIsInstance(self.app.author, Author)
    
    def test_user(self):
        """Тест модели User."""
        self.assertEqual(self.user.id, "user1")
        self.assertEqual(self.user.name, "Алексей")
        
        uc = UserCurrency(user_id="user1", currency_id="USD")
        self.user.add_subscription(uc)
        self.assertIn(uc, self.user.subscriptions)
    
    def test_currency(self):
        """Тест модели Currency."""
        self.assertEqual(self.currency.char_code, "USD")
        self.assertEqual(self.currency.value, 90.1234)
        self.assertEqual(self.currency.nominal, 1)
    
    def test_currency_errors(self):
        """Тест ошибок модели Currency."""
        with self.assertRaises(TypeError):
            Currency(char_code=123)  # Неправильный тип
        with self.assertRaises(ValueError):
            Currency(char_code="AB")  # Неправильная длина
        with self.assertRaises(ValueError):
            Currency(value=-1)  # Отрицательный курс


if __name__ == '__main__':
    unittest.main()
