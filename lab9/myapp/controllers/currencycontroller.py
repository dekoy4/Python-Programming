"""
Контроллер бизнес-логики для валют.
"""

from typing import List, Dict, Any
from controllers.databasecontroller import DatabaseController


class CurrencyController:
    """
    Контроллер для работы с валютами.
    
    Args:
        db_controller: контроллер базы данных
    """
    
    def __init__(self, db_controller: DatabaseController) -> None:
        self.db = db_controller

    def list_currencies(self) -> List[Dict[str, Any]]:
        """
        Получает список всех валют.
        
        Returns:
            List[Dict[str, Any]]: валюты из базы данных
        """
        return self.db.read_currencies()

    def update_currency(self, char_code: str, value: float) -> bool:
        """
        Обновляет курс валюты по коду.
        
        Args:
            char_code: код валюты (USD, EUR и т.д.)
            value: новый курс
            
        Returns:
            bool: результат операции
        """
        return self.db.update_currency_by_code(char_code, value)

    def delete_currency(self, currency_id: int) -> bool:
        """
        Удаляет валюту по ID.
        
        Args:
            currency_id: ID валюты
            
        Returns:
            bool: результат операции
        """
        return self.db.delete_currency(currency_id)
