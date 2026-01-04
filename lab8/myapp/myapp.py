#!/usr/bin/env python3
"""Основной файл веб-приложения по курсам валют."""

import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.currencies_api import get_currencies, get_currency_history
from models.author import Author
from models.app import App
from models.user import User
from models.user_currency import UserCurrency

class CurrencyAppHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов для приложения."""
    
    # ГЛОБАЛЬНЫЕ данные (один раз при запуске сервера)
    main_author = None
    myapp = None
    users = None
    env = None
    templates = None
    
    @classmethod
    def initialize_data(cls):
        """Инициализация данных один раз."""
        if cls.main_author is None:
            cls.main_author = Author("Юльякшин Анатолий", "P4150")
            cls.myapp = App("Валютный лист", "1.0.1", cls.main_author)
            
            cls.users = [
                User("user1", "Алексей Петров"),
                User("user2", "Мария Сидорова"),
            ]
            
            uc1 = UserCurrency(user_id="user1", currency_id="USD")
            cls.users[0].add_subscription(uc1)
            
            cls.env = Environment(
                loader=FileSystemLoader("templates"),
                autoescape=select_autoescape()
            )
            cls.templates = {
                'index': cls.env.get_template("index.html"),
                'users': cls.env.get_template("users.html"),
                'currencies': cls.env.get_template("currencies.html"),
                'user': cls.env.get_template("user.html"),
            }
    
    def do_GET(self) -> None:
        """Обработка GET-запросов."""
        # Инициализация при первом запросе
        CurrencyAppHandler.initialize_data()
        
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
        """Главная страница."""
        html_content = CurrencyAppHandler.templates['index'].render(
            myapp=CurrencyAppHandler.myapp.name,
            version=CurrencyAppHandler.myapp.version,
            author_name=CurrencyAppHandler.main_author.name,
            group=CurrencyAppHandler.main_author.group,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_users(self) -> None:
        """Страница пользователей."""
        users_data = [{'id': user.id, 'name': user.name} for user in CurrencyAppHandler.users]
        html_content = CurrencyAppHandler.templates['users'].render(
            users=users_data,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_currencies(self) -> None:
        """Страница валют."""
        try:
            currency_data = get_currencies(['USD', 'EUR', 'GBP'])
            currencies = []
            currency_names = {
                'USD': 'Доллар США', 'EUR': 'Евро', 'GBP': 'Фунт стерлингов'
            }
            for code, value in currency_data.items():
                currencies.append({
                    'char_code': code,
                    'name': currency_names.get(code, 'Неизвестная валюта'),
                    'value': value,
                    'nominal': 1
                })
        except:
            currencies = []
        
        html_content = CurrencyAppHandler.templates['currencies'].render(
            currencies=currencies,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_user(self) -> None:
        """Страница пользователя с графиками."""
        import urllib.parse
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        user_id = query_params.get('id', [''])[0]
        
        user = next((u for u in CurrencyAppHandler.users if u.id == user_id), None)
        if not user:
            self.handle_404()
            return
        
        subscriptions = [{'currency_id': sub.currency_id} for sub in user.subscriptions]
        
        # ГРАФИКИ: История курсов для подписок пользователя
        charts_data = []
        for sub in subscriptions:
            history = get_currency_history(sub['currency_id'])
            charts_data.append({
                'currency': sub['currency_id'],
                'history': history
            })
        
        html_content = CurrencyAppHandler.templates['user'].render(
            user=user, 
            subscriptions=subscriptions,
            charts_data=charts_data,
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'}
            ]
        )
        self._send_html_response(html_content)
    
    def handle_author(self) -> None:
        """Страница автора."""
        html_content = f"""
        <!DOCTYPE html>
        <html><head><title>Автор</title><link rel="stylesheet" href="/static/style.css"></head>
        <body>
            <nav>
                <a href="/">Главная</a>
                <a href="/users">Пользователи</a>
                <a href="/currencies">Валюты</a>
            </nav>
            <h1>Автор приложения</h1>
            <p>Имя: {CurrencyAppHandler.main_author.name}</p>
            <p>Группа: {CurrencyAppHandler.main_author.group}</p>
            <a href="/">← На главную</a>
        </body></html>
        """
        self._send_html_response(html_content)
    
    def handle_static(self) -> None:
        """Статические файлы."""
        file_path = self.path[1:]
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            if file_path.endswith('.css'):
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.handle_404()
    
    def handle_404(self) -> None:
        """404 ошибка."""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>404 Not Found</h1>")
    
    def _send_html_response(self, html_content: str) -> None:
        """Отправка HTML."""
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
