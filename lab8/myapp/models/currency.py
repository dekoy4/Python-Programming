"""Модель валюты."""

from typing import Optional


class Currency:
    """Класс для представления валюты."""
    
    def __init__(self, currency_id: Optional[str] = None, 
                 num_code: Optional[str] = None,
                 char_code: str = "",
                 name: Optional[str] = None,
                 value: Optional[float] = None,
                 nominal: Optional[int] = None) -> None:
        """Инициализация валюты.
        
        Args:
            currency_id: Уникальный идентификатор
            num_code: Цифровой код
            char_code: Символьный код
            name: Название валюты
            value: Курс
            nominal: Номинал
            
        Raises:
            TypeError: Если параметры неверного типа
        """
        self._id: Optional[str] = None
        self._num_code: Optional[str] = None
        self._char_code: Optional[str] = None
        self._name: Optional[str] = None
        self._value: Optional[float] = None
        self._nominal: Optional[int] = None
        
        if currency_id is not None:
            self.id = currency_id
        if num_code is not None:
            self.num_code = num_code
        if char_code:
            self.char_code = char_code
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if nominal is not None:
            self.nominal = nominal
    
    @property
    def id(self) -> Optional[str]:
        """Уникальный идентификатор валюты."""
        return self._id
    
    @id.setter
    def id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("ID must be str")
        self._id = value.strip()
    
    @property
    def num_code(self) -> Optional[str]:
        """Цифровой код валюты."""
        return self._num_code
    
    @num_code.setter
    def num_code(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("NumCode must be str")
        self._num_code = value.strip()
    
    @property
    def char_code(self) -> str:
        """Символьный код валюты."""
        if self._char_code is None:
            raise ValueError("CharCode not set")
        return self._char_code
    
    @char_code.setter
    def char_code(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("CharCode must be str")
        if len(value.strip()) != 3:
            raise ValueError("CharCode must be 3 characters")
        self._char_code = value.strip().upper()
    
    @property
    def name(self) -> Optional[str]:
        """Название валюты."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Name must be str")
        self._name = value.strip()
    
    @property
    def value(self) -> Optional[float]:
        """Курс валюты."""
        return self._value
    
    @value.setter
    def value(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be number")
        if value < 0:
            raise ValueError("Value cannot be negative")
        self._value = float(value)
    
    @property
    def nominal(self) -> Optional[int]:
        """Номинал валюты."""
        return self._nominal
    
    @nominal.setter
    def nominal(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Nominal must be int")
        if value <= 0:
            raise ValueError("Nominal must be positive")
        self._nominal = value
