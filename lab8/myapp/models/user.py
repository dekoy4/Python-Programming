"""Модель пользователя."""

from typing import Optional, List
from .user_currency import UserCurrency


class User:
    """Класс для представления пользователя."""
    
    def __init__(self, user_id: str, name: str) -> None:
        """Инициализация пользователя.
        
        Args:
            user_id: Уникальный идентификатор
            name: Имя пользователя
            
        Raises:
            TypeError: Если параметры неверного типа
            ValueError: Если параметры некорректны
        """
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._subscriptions: List[UserCurrency] = []
        
        self.id = user_id
        self.name = name
    
    @property
    def id(self) -> str:
        """Уникальный идентификатор пользователя."""
        if self._id is None:
            raise ValueError("ID not set")
        return self._id
    
    @id.setter
    def id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("ID must be str")
        if not value.strip():
            raise ValueError("ID cannot be empty")
        self._id = value.strip()
    
    @property
    def name(self) -> str:
        """Имя пользователя."""
        if self._name is None:
            raise ValueError("Name not set")
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Name must be str")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def subscriptions(self) -> List[UserCurrency]:
        """Список подписок пользователя на валюты."""
        return self._subscriptions.copy()
    
    def add_subscription(self, subscription: UserCurrency) -> None:
        """Добавить подписку на валюту.
        
        Args:
            subscription: Объект UserCurrency
        """
        if not isinstance(subscription, UserCurrency):
            raise TypeError("Subscription must be UserCurrency instance")
        if subscription not in self._subscriptions:
            self._subscriptions.append(subscription)
    
    def remove_subscription(self, subscription: UserCurrency) -> None:
        """Удалить подписку на валюту.
        
        Args:
            subscription: Объект UserCurrency
        """
        if subscription in self._subscriptions:
            self._subscriptions.remove(subscription)
