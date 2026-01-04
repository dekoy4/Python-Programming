#!/usr/bin/env python3
"""Основной файл веб-приложения по курсам валют."""

import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List
from jinja2 import Environment, PackageLoader, select_autoescape

# Импорт моделей
from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies


class CurrencyAppHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов для приложения."""
    
    def __init__(self, *args, **kwargs) -> None:
        """Инициализация обработчика."""
        # Создание тестовых данных
        self.main_author = Author("Иван Иванов", "ИТ-21")
        self.myapp = App("CurrenciesListApp", "1.0.0", self.main_author)
        
        self.users: List[User] = [
            User("user1", "Алексей Петров"),
            User("user2", "Мария Сидорова"),
        ]
        
        # Тестовые подписки
        uc1 = UserCurrency(user_id="user1", currency_id="USD")
        self.users[0].add_subscription(uc1)
        
        super().__init__(*args, **kwargs)
        
        # Инициализация Jinja2 один раз
        self.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=select_autoescape()
        )
        self.templates = {
            'index': self.env.get_template("index.html"),
            'users': self.env.get_template("users.html"),
            'currencies': self.env.get_template("currencies.html"),
            'user': self.env.get_template("user.html"),
        }
    
    def do_GET(self) -> None:
        """Обработка GET-запросов."""
        if self.path == '/':
            self.handle_index()
        elif self.path == '/users':
            self.handle_users()
        elif self.path == '/currencies':
            self.handle_currencies()
        elif self.path.startswith('/user'):
            self.handle_user()
        elif self.path == '/author':
            self.handle_author()
        elif self.path.startswith('/static/'):
            self.handle_static()
        else:
            self.handle_404()
    
    def handle_index(self) -> None:
        """Обработка главной страницы."""
        html_content = self.templates['index'].render(
            myapp=self.myapp.name,
            version=self.myapp.version,
            author_name=self.main_author.name,
            group=self.main_author.group,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_users(self) -> None:
        """Обработка страницы пользователей."""
        users_data = [{'id': user.id, 'name': user.name} for user in self.users]
        
        html_content = self.templates['users'].render(
            users=users_data,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'}
            ]
        )
        self._send_html_response(html_content)
    
def handle_currencies(self) -> None:
    """Обработка страницы валют."""
    try:
        currency_data = get_currencies(['USD', 'EUR', 'GBP', 'IDR'])
        currencies = []
        
        # Словарь с названиями валют для демонстрации
        currency_names = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'GBP': 'Фунт стерлингов',
            'IDR': 'Индонезийская рупия'
        }
        
        for code, value in currency_data.items():
            currency = Currency(char_code=code, value=value, nominal=1)
            currencies.append({
                'char_code': currency.char_code,
                'name': currency_names.get(code, 'Неизвестная валюта'),
                'value': currency.value,
                'nominal': currency.nominal
            })
    except Exception:
        currencies = []
        
        html_content = self.templates['currencies'].render(
            currencies=currencies,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_user(self) -> None:
        """Обработка страницы конкретного пользователя."""
        query_params = urllib.parse.parse_qs(
            urllib.parse.urlparse(self.path).query
        )
        user_id = query_params.get('id', [''])[0]
        
        user = next((u for u in self.users if u.id == user_id), None)
        if not user:
            self.handle_404()
            return
        
        subscriptions = [
            {'currency_id': sub.currency_id} 
            for sub in user.subscriptions
        ]
        
        html_content = self.templates['user'].render(
            user=user,
            subscriptions=subscriptions,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_author(self) -> None:
        """Обработка страницы автора."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Автор</title></head>
        <body>
            <h1>Автор приложения</h1>
            <p>Имя: {self.main_author.name}</p>
            <p>Группа: {self.main_author.group}</p>
            <a href="/">На главную</a>
        </body>
        </html>
        """
        self._send_html_response(html_content)
    
    def handle_static(self) -> None:
        """Обработка статических файлов."""
        file_path = self.path[1:]  # Убираем начальный слеш
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            if file_path.endswith('.css'):
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
            else:
                self.send_response(200)
            
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.handle_404()
    
    def handle_404(self) -> None:
        """Обработка 404 ошибки."""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>404 Not Found</h1>")
    
    def _send_html_response(self, html_content: str) -> None:
        """Отправить HTML-ответ."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(html_content, 'utf-8'))


def run_server(host: str = 'localhost', port: int = 8000) -> None:
    """Запуск HTTP-сервера."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, CurrencyAppHandler)
    print(f"Сервер запущен на http://{host}:{port}")
    print("Нажмите Ctrl+C для остановки")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
