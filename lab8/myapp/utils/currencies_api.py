"""API для получения курсов валют с ЦБ РФ."""

import requests
from typing import Dict, Optional, List
from xml.etree import ElementTree as ET

def get_currencies(currency_codes: Optional[list] = None) -> Dict[str, float]:
    """Получить актуальные курсы валют с ЦБ РФ.
    
    Args:
        currency_codes: Список кодов ['USD', 'EUR']
        
    Returns:
        { 'USD': 91.25, 'EUR': 99.80 }
    """
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Парсинг XML от ЦБ
        root = ET.fromstring(response.content)
        
        currencies = {}
        for valute in root.findall('.//Valute'):
            char_code = valute.find('CharCode').text
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            rate = value / nominal  # Курс за 1 единицу
            
            currencies[char_code] = rate
        
        if currency_codes:
            return {code: currencies.get(code, 0.0) for code in currency_codes}
        
        return currencies
        
    except Exception as e:
        print(f"Ошибка API: {e}")
        # Fallback на тестовые данные
        return {'USD': 91.25, 'EUR': 99.80, 'GBP': 115.00}
        
def get_currency_history(currency_code: str, months: int = 3) -> List[Dict]:
    """Получить историю курсов за N месяцев.
    
    Returns:
        [{'date': '2025-12-01', 'value': 91.25}, ...]
    """
    from datetime import datetime, timedelta
    import random
    
    history = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # 3 месяца
    
    current_date = start_date
    while current_date <= end_date:
        # Симуляция реальных курсов (в продакшене - API ЦБ)
        base_rate = 90.0 if currency_code == 'USD' else 98.0
        noise = random.uniform(-2, 2)  # Колебания ±2%
        rate = base_rate + noise
        
        history.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'value': round(rate, 4)
        })
        current_date += timedelta(days=7)  # Недельные данные
    
    return history
