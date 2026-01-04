"""Модель связи пользователь-валюта."""

from typing import Optional


class UserCurrency:
    """Класс для связи между пользователем и валютой."""
    
    def __init__(self, uc_id: Optional[str] = None,
                 user_id: Optional[str] = None,
                 currency_id: Optional[str] = None) -> None:
        """Инициализация связи пользователь-валюта.
        
        Args:
            uc_id: Уникальный идентификатор связи
            user_id: ID пользователя
            currency_id: ID валюты
            
        Raises:
            TypeError: Если параметры неверного типа
        """
        self._id: Optional[str] = None
        self._user_id: Optional[str] = None
        self._currency_id: Optional[str] = None
        
        if uc_id is not None:
            self.id = uc_id
        if user_id is not None:
            self.user_id = user_id
        if currency_id is not None:
            self.currency_id = currency_id
    
    @property
    def id(self) -> Optional[str]:
        """Уникальный идентификатор связи."""
        return self._id
    
    @id.setter
    def id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("ID must be str")
        self._id = value.strip()
    
    @property
    def user_id(self) -> Optional[str]:
        """ID пользователя."""
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("User ID must be str")
        self._user_id = value.strip()
    
    @property
    def currency_id(self) -> Optional[str]:
        """ID валюты."""
        return self._currency_id
    
    @currency_id.setter
    def currency_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Currency ID must be str")
        self._currency_id = value.strip()
