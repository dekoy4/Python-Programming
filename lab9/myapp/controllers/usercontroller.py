"""
Контроллер бизнес-логики для пользователей.
"""

from typing import List, Dict, Any
from controllers.databasecontroller import DatabaseController


class UserController:
    """
    Контроллер для работы с пользователями.
    
    Args:
        db_controller: контроллер базы данных
    """
    
    def __init__(self, db_controller: DatabaseController) -> None:
        self.db = db_controller

    def list_users(self) -> List[Dict[str, Any]]:
        """
        Получает список всех пользователей.
        
        Returns:
            List[Dict[str, Any]]: пользователи
        """
        return self.db.get_users()
