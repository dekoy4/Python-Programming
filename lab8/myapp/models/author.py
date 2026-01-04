"""Модель автора приложения."""

from typing import Optional


class Author:
    """Класс для представления автора приложения."""
    
    def __init__(self, name: str, group: str) -> None:
        """Инициализация автора.
        
        Args:
            name: Имя автора
            group: Учебная группа
            
        Raises:
            TypeError: Если параметры неверного типа
            ValueError: Если параметры пустые
        """
        self._name: Optional[str] = None
        self._group: Optional[str] = None
        
        self.name = name
        self.group = group
    
    @property
    def name(self) -> str:
        """Имя автора."""
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
    def group(self) -> str:
        """Учебная группа автора."""
        if self._group is None:
            raise ValueError("Group not set")
        return self._group
    
    @group.setter
    def group(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Group must be str")
        if not value.strip():
            raise ValueError("Group cannot be empty")
        self._group = value.strip()
