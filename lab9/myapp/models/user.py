"""
Модель пользователя.
"""

from typing import List, Optional
from models.currency import Currency


class User:
    """
    Модель пользователя с подписками на валюты.
    
    Args:
        name: имя пользователя
        user_id: ID в базе данных (опционально)
    """
    
    def __init__(self, name: str, user_id: Optional[int] = None):
        self._id: Optional[int] = user_id
        self._name: str = name
        self._currencies: List[Currency] = []

    @property
    def id(self) -> Optional[int]:
        """ID пользователя."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if value < 1:
            raise ValueError("ID должен быть положительным")
        self._id = value

    @property
    def name(self) -> str:
        """Имя пользователя."""
        return self._name

    @property
    def currencies(self) -> List[Currency]:
        """Список подписанных валют."""
        return self._currencies.copy()

    def add_currency(self, currency: Currency) -> None:
        """
        Добавляет валюту в подписки пользователя.
        
        Args:
            currency: валюта для подписки
        """
        if currency not in self._currencies:
            self._currencies.append(currency)

    def to_dict(self) -> dict:
        """
        Преобразует объект в словарь.
        
        Returns:
            dict: данные пользователя
        """
        return {
            'id': self._id,
            'name': self._name
        }

    def __repr__(self) -> str:
        return f"User(id={self._id}, name='{self._name}')"
