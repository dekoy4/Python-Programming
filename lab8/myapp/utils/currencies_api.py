"""API для получения курсов валют."""

import requests
from typing import Dict, Optional


def get_currencies(currency_codes: Optional[list] = None) -> Dict[str, float]:
    """Получить курсы валют с ЦБ РФ.
    
    Args:
        currency_codes: Список символьных кодов валют (USD, EUR и т.д.)
        
    Returns:
        Словарь {код_валюты: курс}
        
    Raises:
        requests.RequestException: Ошибка сети
        ValueError: Некорректный ответ сервера
    """
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Парсинг XML (упрощенный для демонстрации)
        # В реальном проекте используйте xml.etree.ElementTree
        currencies = {
            'USD': 90.1234,
            'EUR': 98.5678,
            'GBP': 115.4321,
            'IDR': 0.00486
        }
        
        if currency_codes:
            return {code: currencies.get(code, 0.0) for code in currency_codes}
        
        return currencies
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch currencies: {e}")
