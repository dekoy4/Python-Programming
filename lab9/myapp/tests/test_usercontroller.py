"""
Unit-тесты для UserController.
"""

import unittest
from unittest.mock import MagicMock
from controllers.usercontroller import UserController


class TestUserController(unittest.TestCase):
    """Тесты контроллера пользователей."""

    def setUp(self) -> None:
        self.mock_db = MagicMock()

    def test_list_users(self) -> None:
        """Тест получения списка пользователей."""
        expected_users = [
            {"id": 1, "name": "Иван"},
            {"id": 2, "name": "Мария"}
        ]
        self.mock_db.get_users.return_value = expected_users
        
        controller = UserController(self.mock_db)
        result = controller.list_users()
        
        self.assertEqual(result, expected_users)
        self.mock_db.get_users.assert_called_once()


if __name__ == '__main__':
    unittest.main()
