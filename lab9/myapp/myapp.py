"""
Главное веб-приложение с архитектурой MVC для работы с валютами и пользователями.
Использует SQLite в памяти и Jinja2 для рендеринга шаблонов.
"""

import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
import os

from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.pages import PagesController


🔧 Исправление NameError: name 'self' is not defined
Проблема: В коде есть статический код (не внутри метода класса), где используется self.path, но self доступен только внутри методов класса.

Ошибка на строке 27 указывает, что parsed_url = urlparse(self.path) находится вне метода.

Правильная структура класса RouterHandler
Замените ВЕСЬ класс RouterHandler (строки 18-120) на этот исправленный код:

python
class RouterHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов с маршрутизацией."""
    
    def __init__(self, *args, controllers=None, **kwargs):
        self.controllers = controllers
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        """Обработка GET-запросов с маршрутизацией."""
        from urllib.parse import urlparse, parse_qs  # Импорт внутри метода
        
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        try:
            if parsed_url.path == '/':
                self.handle_index(query_params)
            elif parsed_url.path == '/author':
                self.handle_author()
            elif parsed_url.path == '/users':
                self.handle_users()
            elif parsed_url.path == '/user' and 'id' in query_params:
                self.handle_user(query_params['id'][0])
            elif parsed_url.path == '/currencies':
                self.handle_currencies()
            elif parsed_url.path == '/currency/delete' and 'id' in query_params:
                self.handle_delete_currency(query_params['id'][0])
            elif parsed_url.path == '/currency/update':
                self.handle_update_currency(query_params)
            elif parsed_url.path == '/currency/show':
                self.handle_show_currencies()
            else:
                self.send_error(404, "Page not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def handle_index(self, query_params: dict) -> None:
        """Обработчик главной страницы."""
        subscribed_currencies = self.controllers['pages'].get_subscribed_currencies()
        self.render_template('index.html', {'currencies': subscribed_currencies})

    def handle_author(self) -> None:
        """Обработчик страницы автора."""
        self.render_template('author.html')

    def handle_users(self) -> None:
        """Обработчик списка пользователей."""
        users = self.controllers['pages'].get_users()
        self.render_template('users.html', {'users': users})

    def handle_user(self, user_id: str) -> None:
        """Обработчик страницы конкретного пользователя."""
        user_currencies = self.controllers['pages'].get_user_currencies(int(user_id))
        self.render_template('user.html', {'user_id': user_id, 'currencies': user_currencies})

    def handle_currencies(self) -> None:
        """Обработчик списка всех валют."""
        currencies = self.controllers['currency'].list_currencies()
        self.render_template('currencies.html', {'currencies': currencies})

    def handle_delete_currency(self, currency_id: str) -> None:
        """Обработчик удаления валюты."""
        self.controllers['currency'].delete_currency(int(currency_id))
        self.send_response(302)
        self.send_header('Location', '/currencies')
        self.end_headers()

    def handle_update_currency(self, query_params: dict) -> None:
        """Обработчик обновления курса валюты."""
        for char_code, values in query_params.items():
            if len(values) == 1 and char_code.isalpha() and len(char_code) == 3:
                try:
                    value = float(values[0])
                    self.controllers['currency'].update_currency(char_code, value)
                except ValueError:
                    pass
        self.send_response(302)
        self.send_header('Location', '/currencies')
        self.end_headers()

    def handle_show_currencies(self) -> None:
        """Отладочный обработчик - вывод валют в консоль."""
        currencies = self.controllers['currency'].list_currencies()
        print("=== Все валюты ===")
        for currency in currencies:
            print(currency)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        message = "Валюты выведены в консоль. Проверьте терминал."
        self.wfile.write(message.encode('utf-8'))

    def render_template(self, template_name: str, context: dict = None) -> None:
        """Рендеринг HTML-шаблона."""
        if context is None:
            context = {}
        
        template = self.server.template_env.get_template(template_name)
        html_content = template.render(**context)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


def create_app() -> tuple[HTTPServer, dict]:
    """
    Создает и инициализирует веб-приложение.
    
    Returns:
        tuple[HTTPServer, dict]: HTTP-сервер и словарь контроллеров
    """
    # Инициализация Jinja2
    env = Environment(loader=FileSystemLoader('templates'), 
                     keep_trailing_newline=True)
    
    # Инициализация базы данных
    db_controller = DatabaseController()
    
    # Создание контроллеров
    currency_controller = CurrencyController(db_controller)
    user_controller = UserController(db_controller)
    pages_controller = PagesController(db_controller, env)
    
    controllers = {
        'currency': currency_controller,
        'user': user_controller,
        'pages': pages_controller
    }
    
    # Создание сервера
    server = HTTPServer(('localhost', 8000), lambda *args, **kwargs: 
                       RouterHandler(*args, controllers=controllers, **kwargs))
    server.template_env = env
    
    return server, controllers


def main() -> None:
    """Запуск веб-приложения."""
    server, controllers = create_app()
    print("Сервер запущен на http://localhost:8000")
    print("Доступные маршруты:")
    print("  / - Главная")
    print("  /author - Об авторе")
    print("  /users - Пользователи")
    print("  /currencies - Все валюты")
    print("  /currency/show - Показать валюты в консоли")
    server.serve_forever()


if __name__ == '__main__':
    main()
