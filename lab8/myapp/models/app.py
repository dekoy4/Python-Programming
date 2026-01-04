"""Модель приложения."""

from typing import Optional
from .author import Author


class App:
    """Класс для представления приложения."""
    
    def __init__(self, name: str, version: str, author: Author) -> None:
        """Инициализация приложения.
        
        Args:
            name: Название приложения
            version: Версия приложения
            author: Объект Author
            
        Raises:
            TypeError: Если параметры неверного типа
            ValueError: Если параметры некорректны
        """
        self._name: Optional[str] = None
        self._version: Optional[str] = None
        self._author: Optional[Author] = None
        
        self.name = name
        self.version = version
        self.author = author
    
    @property
    def name(self) -> str:
        """Название приложения."""
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
    def version(self) -> str:
        """Версия приложения."""
        if self._version is None:
            raise ValueError("Version not set")
        return self._version
    
    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Version must be str")
        if not value.strip():
            raise ValueError("Version cannot be empty")
        self._version = value.strip()
    
    @property
    def author(self) -> Author:
        """Автор приложения."""
        if self._author is None:
            raise ValueError("Author not set")
        return self._author
    
    @author.setter
    def author(self, value: Author) -> None:
        if not isinstance(value, Author):
            raise TypeError("Author must be Author instance")
        self._author = value
