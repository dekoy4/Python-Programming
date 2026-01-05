"""
Контроллер работы с базой данных SQLite.
Реализует CRUD операции с защитой от SQL-инъекций.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager


class DatabaseController:
    """
    Контроллер базы данных SQLite в памяти.
    Управляет таблицами user, currency и user_currency.
    """

    def __init__(self) -> None:
        """
        Инициализирует базу данных в памяти и создает таблицы.
        Заполняет тестовыми данными.
        """
        self._conn = sqlite3.connect(':memory:')
        self._conn.row_factory = sqlite3.Row  # Возвращает словари вместо кортежей
        self._init_database()
        self._populate_test_data()

    @contextmanager
    def _get_cursor(self):
        """Контекстный менеджер для курсора."""
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def _init_database(self) -> None:
        """
        Создает структуру базы данных с первичными и внешними ключами.
        Первичный ключ (PRIMARY KEY) - уникальный идентификатор записи.
        Внешний ключ (FOREIGN KEY) - обеспечивает целостность ссылок между таблицами.
        """
        with self._get_cursor() as cursor:
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

            # Таблица валют
            cursor.execute("""
                CREATE TABLE currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num_code TEXT NOT NULL,
                    char_code TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    nominal INTEGER NOT NULL
                )
            """)

            # Связующая таблица многие-ко-многим
            cursor.execute("""
                CREATE TABLE user_currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    currency_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                    FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE,
                    UNIQUE(user_id, currency_id)
                )
            """)

    def _populate_test_data(self) -> None:
        """Заполняет базу тестовыми данными."""
        test_users = [
            ("Иван",),
            ("Мария",),
            ("Петр",)
        ]

        test_currencies = [
            ("840", "USD", "Доллар США", 90.5, 1),
            ("978", "EUR", "Евро", 98.2, 1),
            ("643", "RUB", "Российский рубль", 1.0, 1),
            ("398", "KZT", "Казахстанский тенге", 0.21, 1)
        ]

        with self._get_cursor() as cursor:
            cursor.executemany("INSERT INTO user (name) VALUES (?)", test_users)
            cursor.executemany(
                "INSERT INTO currency (num_code, char_code, name, value, nominal) "
                "VALUES (?, ?, ?, ?, ?)",
                test_currencies
            )

            # Подписки пользователей на валюты
            subscriptions = [
                (1, 1),  # Иван -> USD
                (1, 2),  # Иван -> EUR
                (2, 1),  # Мария -> USD
                (3, 3)   # Петр -> RUB
            ]
            cursor.executemany(
                "INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)",
                subscriptions
            )

    def create_currency(self, currency_data: Dict[str, Any]) -> int:
        """
        Создает новую валюту.
        
        Args:
            currency_data: данные валюты
            
        Returns:
            int: ID созданной валюты
        """
        sql = """
            INSERT INTO currency (num_code, char_code, name, value, nominal)
            VALUES (:num_code, :char_code, :name, :value, :nominal)
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql, currency_data)
            return cursor.lastrowid

    def read_currencies(self) -> List[Dict[str, Any]]:
        """
        Читает все валюты из базы.
        
        Returns:
            List[Dict[str, Any]]: список валют
        """
        with self._get_cursor() as cursor:
            cursor.execute("SELECT * FROM currency ORDER BY char_code")
            return [dict(row) for row in cursor.fetchall()]

    def update_currency_value(self, currency_id: int, value: float) -> bool:
        """
        Обновляет курс валюты по ID.
        
        Args:
            currency_id: ID валюты
            value: новый курс
            
        Returns:
            bool: True если обновление прошло успешно
        """
        sql = "UPDATE currency SET value = ? WHERE id = ?"
        with self._get_cursor() as cursor:
            result = cursor.execute(sql, (value, currency_id))
            return result.rowcount > 0

    def update_currency_by_code(self, char_code: str, value: float) -> bool:
        """
        Обновляет курс валюты по коду.
        
        Args:
            char_code: код валюты
            value: новый курс
            
        Returns:
            bool: True если обновление прошло успешно
        """
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        with self._get_cursor() as cursor:
            result = cursor.execute(sql, (value, char_code))
            return result.rowcount > 0

    def delete_currency(self, currency_id: int) -> bool:
        """
        Удаляет валюту по ID.
        
        Args:
            currency_id: ID валюты
            
        Returns:
            bool: True если удаление прошло успешно
        """
        sql = "DELETE FROM currency WHERE id = ?"
        with self._get_cursor() as cursor:
            result = cursor.execute(sql, (currency_id,))
            return result.rowcount > 0

    def get_users(self) -> List[Dict[str, Any]]:
        """Возвращает всех пользователей."""
        with self._get_cursor() as cursor:
            cursor.execute("SELECT id, name FROM user ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Возвращает валюты пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            List[Dict[str, Any]]: валюты пользователя
        """
        sql = """
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
            ORDER BY c.char_code
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_subscribed_currencies(self) -> List[Dict[str, Any]]:
        """
        Возвращает популярные валюты (на которые есть подписки).
        
        Returns:
            List[Dict[str, Any]]: популярные валюты
        """
        sql = """
            SELECT c.*, COUNT(uc.id) as subscribers
            FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            GROUP BY c.id
            ORDER BY subscribers DESC, c.char_code
            LIMIT 5
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
