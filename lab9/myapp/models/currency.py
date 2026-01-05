"""
Модель валюты с валидацией данных.
"""

from typing import Optional


class Currency:
    """
    Модель валюты с приватными атрибутами и валидацией.
    
    Args:
        num_code: цифровой код валюты (например, "840")
        char_code: буквенный код валюты (например, "USD")
        name: название валюты
        value: курс валюты
        nominal: номинал
        currency_id: ID в базе данных (опционально)
    """
    
    def __init__(self, num_code: str, char_code: str, name: str, 
                 value: float, nominal: int, currency_id: Optional[int] = None):
        self._id: Optional[int] = currency_id
        self._num_code: str = num_code
        self.char_code = char_code  # триггерит setter
        self._name: str = name
        self.value = value  # триггерит setter
        self._nominal: int = nominal

    @property
    def id(self) -> Optional[int]:
        """ID валюты в базе данных."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if value < 1:
            raise ValueError("ID должен быть положительным")
        self._id = value

    @property
    def num_code(self) -> str:
        """Цифровой код валюты."""
        return self._num_code

    @property
    def char_code(self) -> str:
        """Буквенный код валюты."""
        return self._char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        """
        Устанавливает буквенный код валюты с валидацией.
        
        Args:
            value: код из 3 букв (например, "USD")
            
        Raises:
            ValueError: если код не состоит из 3 символов
        """
        if len(value) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self._char_code = value.upper()

    @property
    def name(self) -> str:
        """Название валюты."""
        return self._name

    @property
    def value(self) -> float:
        """Курс валюты."""
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        """
        Устанавливает курс валюты с валидацией.
        
        Args:
            new_value: новый курс
            
        Raises:
            ValueError: если курс отрицательный
        """
        if new_value < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self._value = new_value

    @property
    def nominal(self) -> int:
        """Номинал валюты."""
        return self._nominal

    def to_dict(self) -> dict:
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            dict: данные валюты
        """
        result = {
            'id': self._id,
            'num_code': self._num_code,
            'char_code': self._char_code,
            'name': self._name,
            'value': self._value,
            'nominal': self._nominal
        }
        return result

    def __repr__(self) -> str:
        return (f"Currency(id={self._id}, char_code='{self._char_code}', "
                f"value={self._value}, name='{self._name}')")
