"""
Unit-тесты для CurrencyController с использованием unittest.mock.
"""

import unittest
from unittest.mock import MagicMock, patch
from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import DatabaseController


class TestCurrencyController(unittest.TestCase):
    """Тесты контроллера валют."""

    def setUp(self) -> None:
        """Создает мок для базы данных перед каждым тестом."""
        self.mock_db = MagicMock(spec=DatabaseController)

    def test_list_currencies(self) -> None:
        """Тест получения списка валют."""
        # Arrange
        expected_currencies = [
            {"id": 1, "char_code": "USD", "value": 90.0},
            {"id": 2, "char_code": "EUR", "value": 98.0}
        ]
        self.mock_db.read_currencies.return_value = expected_currencies
        
        controller = CurrencyController(self.mock_db)
        
        # Act
        result = controller.list_currencies()
        
        # Assert
        self.assertEqual(result, expected_currencies)
        self.mock_db.read_currencies.assert_called_once()

    def test_update_currency_success(self) -> None:
        """Тест успешного обновления курса."""
        # Arrange
        self.mock_db.update_currency_by_code.return_value = True
        
        controller = CurrencyController(self.mock_db)
        
        # Act
        result = controller.update_currency("USD", 95.5)
        
        # Assert
        self.assertTrue(result)
        self.mock_db.update_currency_by_code.assert_called_once_with("USD", 95.5)

    def test_update_currency_failure(self) -> None:
        """Тест неудачного обновления курса."""
        # Arrange
        self.mock_db.update_currency_by_code.return_value = False
        
        controller = CurrencyController(self.mock_db)
        
        # Act
        result = controller.update_currency("USD", 95.5)
        
        # Assert
        self.assertFalse(result)
        self.mock_db.update_currency_by_code.assert_called_once_with("USD", 95.5)

    def test_delete_currency(self) -> None:
        """Тест удаления валюты."""
        # Arrange
        self.mock_db.delete_currency.return_value = True
        
        controller = CurrencyController(self.mock_db)
        
        # Act
        result = controller.delete_currency(1)
        
        # Assert
        self.assertTrue(result)
        self.mock_db.delete_currency.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
