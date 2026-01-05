"""
Контроллер рендеринга страниц.
"""

from typing import List, Dict, Any
from jinja2 import Environment
from controllers.databasecontroller import DatabaseController


class PagesController:
    """
    Контроллер для подготовки данных страниц.
    
    Args:
        db_controller: контроллер базы данных
        template_env: окружение Jinja2
    """
    
    def __init__(self, db_controller: DatabaseController, 
                 template_env: Environment) -> None:
        self.db = db_controller
        self.template_env = template_env

    def get_users(self) -> List[Dict[str, Any]]:
        """Получает данные для страницы пользователей."""
        return self.db.get_users()

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Получает валюты конкретного пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            List[Dict[str, Any]]: валюты пользователя
        """
        return self.db.get_user_currencies(user_id)

    def get_subscribed_currencies(self) -> List[Dict[str, Any]]:
        """
        Получает популярные валюты для главной страницы.
        
        Returns:
            List[Dict[str, Any]]: топ-5 валют по популярности
        """
        return self.db.get_subscribed_currencies()
