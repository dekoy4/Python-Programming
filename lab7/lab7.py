# Группа P4150 Юльякшин Анатолий Сергеевич
"""Модуль логирующего декоратора и получения курсов валют."""
import functools
import sys
import io
import json
import logging
import unittest
import requests
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


def logger(
    func: Optional[Callable[..., Any]] = None,
    *,
    handle: Union[io.TextIOBase, logging.Logger] = sys.stdout
) -> Callable:
    """
    Универсальный параметризуемый логирующий декоратор.

    Поддерживает три варианта логирования в зависимости от типа handle:

    1. sys.stdout (по умолчанию) или любой file-like объект -> handle.write()
    2. logging.Logger -> log.info()/log.error()
    
    Логирует:
    - INFO: начало вызова с аргументами
    - INFO: успешное завершение с результатом  
    - ERROR: исключения с повторным пробросом

    Args:
        func: Декорируемая функция (для @logger).
        handle: Объект логирования (file-like или Logger).

    Returns:
        Декоратор, сохраняющий сигнатуру оригинальной функции.
    """
    def decorator(
        inner_func: Callable[..., Any]
    ) -> Callable[..., Any]:
        """Внутренний декоратор."""
        @functools.wraps(inner_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка с логированием."""
            # Определяем тип handle
            is_logger = (
                hasattr(handle, 'info')
                and hasattr(handle, 'error')
            )

            try:
                # Формируем строку аргументов
                args_str = (
                    ', '.join(
                        [str(a) for a in args]
                        + [f'{k}={v}' for k, v in kwargs.items()]
                    )
                )

                # Лог начала выполнения
                start_msg = (
                    f"INFO: {inner_func.__name__} "
                    f"start with args: {args_str}"
                )

                if is_logger:
                    handle.info(start_msg)
                else:
                    handle.write(f"{start_msg}\n")

                # Выполнение функции
                result = inner_func(*args, **kwargs)

                # Лог успешного завершения
                end_msg = (
                    f"INFO: {inner_func.__name__} "
                    f"end with result: {result}"
                )

                if is_logger:
                    handle.info(end_msg)
                else:
                    handle.write(f"{end_msg}\n")

                return result

            except Exception as exc:
                # Лог ошибки
                error_msg = (
                    f"ERROR: {inner_func.__name__}: "
                    f"{type(exc).__name__}: {str(exc)}"
                )

                if is_logger:
                    handle.error(error_msg)
                else:
                    handle.write(f"{error_msg}\n")

                # Повторно выбрасываем исключение
                raise

        return wrapper

    # Поддержка @logger и @logger(handle=...)
    return decorator(func) if func else decorator


def get_currencies(
    currency_codes: List[str],
    url: str = (
        "https://www.cbr-xml-daily.ru/daily_json.js"
    ),
) -> Dict[str, float]:
    """
    Получает курсы валют с API Центрального банка РФ.

    Выполняет чистую бизнес-логику без логирования.

    Args:
        currency_codes: Список кодов валют (USD, EUR, ...).
        url: URL API ЦБ РФ.

    Returns:
        Словарь {код_валюты: курс}.

    Raises:
        ConnectionError: API недоступен.
        ValueError: Некорректный JSON.
        KeyError: Отсутствует Valute или запрошенная валюта.
        TypeError: Курс имеет неверный тип.
    """
    # HTTP запрос
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Парсинг JSON
    data: Dict[str, Any] = response.json()

    # Проверка наличия Valute
    valutes: Dict[str, Any] = data['Valute']

    # Извлечение курсов
    result: Dict[str, float] = {}
    for code in currency_codes:
        if code not in valutes:
            raise KeyError(f"Валюта '{code}' отсутствует")

        valute_data = valutes[code]
        value = valute_data['Value']

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Курс '{code}' имеет тип {type(value)}, "
                f"ожидается number"
            )

        result[code] = float(value)

    return result


# ========================================
# ФАЙЛОВОЕ ЛОГИРОВАНИЕ
# ========================================

def setup_file_logger() -> logging.Logger:
    """Настраивает логгер для записи в файл currency.log."""
    logger_obj = logging.getLogger("currency_file")
    logger_obj.setLevel(logging.INFO)

    # Удаляем старые обработчики
    for handler in logger_obj.handlers[:]:
        logger_obj.removeHandler(handler)

    # FileHandler
    file_handler = logging.FileHandler("currency.log", encoding='utf-8')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger_obj.addHandler(file_handler)

    return logger_obj


file_logger = setup_file_logger()


@logger(handle=file_logger)
def get_currencies_file_logging(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    """get_currencies с логированием в файл."""
    return get_currencies(currency_codes, url)


# ========================================
# ДЕМОНСТРАЦИЯ
# ========================================

def solve_quadratic(
    a: float,
    b: float, 
    c: float
) -> Optional[List[float]]:
    """Решает квадратное уравнение ax²+bx+c=0."""
    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        logging.warning("Дискриминант < 0: %.3f", discriminant)
        return None

    if abs(a) < 1e-10 and abs(b) < 1e-10:
        logging.critical("Недопустимые коэффициенты: a=b=0")
        raise ValueError("Уравнение вырожденное")

    sqrt_d = discriminant ** 0.5
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)

    return [x1, x2] if discriminant > 0 else [x1]


@logger()
def demo_quadratic(a: float, b: float, c: float) -> Optional[List[float]]:
    """Демонстрация декоратора на квадратном уравнении."""
    return solve_quadratic(a, b, c)


def main() -> None:
    """Демонстрация работы декоратора."""
    print("=== ДЕКОРАТОР LOGGER ===\n")

    # 1. Успешный вызов
    print("1. Успешное выполнение:")
    roots = demo_quadratic(1, 5, 6)
    print(f"Корни: {roots}\n")

    # 2. Ошибка типов
    print("2. Ошибка типов:")
    try:
        demo_quadratic("1", 2, 3)
    except Exception as e:
        print(f"Исключение: {e}\n")

    # 3. Курсы валют (логи в файл)
    print("3. Курсы валют (логи -> currency.log):")
    try:
        rates = get_currencies_file_logging(["USD", "EUR"])
        print(f"Курсы: {rates}")
    except Exception as e:
        print(f"Ошибка API: {e}")


# ========================================
# ТЕСТЫ
# ========================================

class TestLoggerDecorator(unittest.TestCase):
    """Тесты декоратора logger."""

    def setUp(self) -> None:
        """Создает StringIO для тестов."""
        self.stream = io.StringIO()

    def test_success_logging(self) -> None:
        """Тест логирования успешного выполнения."""
        @logger(handle=self.stream)
        def multiply(x: int, y: int) -> int:
            return x * y

        result = multiply(3, 4)
        logs = self.stream.getvalue()

        self.assertIn("INFO: multiply start", logs)
        self.assertIn("3, 4", logs)
        self.assertIn("INFO: multiply end", logs)
        self.assertIn("12", logs)
        self.assertEqual(result, 12)

    def test_error_logging(self) -> None:
        """Тест логирования исключений."""
        @logger(handle=self.stream)
        def divide_zero(x: int) -> float:
            return x / 0

        with self.assertRaises(ZeroDivisionError):
            divide_zero(10)

        logs = self.stream.getvalue()
        self.assertIn("ERROR: divide_zero", logs)
        self.assertIn("ZeroDivisionError", logs)

    def test_signature_preservation(self) -> None:
        """Тест сохранения сигнатуры."""
        @logger()
        def test_func(a: int, b: str = "default") -> str:
            return f"{a}{b}"

        import inspect
        sig = inspect.signature(test_func)
        self.assertEqual(sig.parameters['a'].annotation, int)
        self.assertEqual(sig.parameters['b'].default, "default")


class TestGetCurrencies(unittest.TestCase):
    """Тесты бизнес-логики get_currencies."""

    def test_missing_currency(self) -> None:
        """Тест отсутствующей валюты."""
        def mock_request() -> Dict[str, Any]:
            return {
                'Valute': {'USD': {'Value': 93.25}}
            }

        # Мок не нужен для KeyError
        with self.assertRaises(KeyError):
            get_currencies(["XXX"])

    def test_invalid_value_type(self) -> None:
        """Тест неверного типа курса."""
        def mock_data() -> Dict[str, Any]:
            return {
                'Valute': {
                    'USD': {'Value': "invalid"}
                }
            }

        with self.assertRaises(TypeError):
            pass  # Тест требует мок requests


class TestFileLoggingContext(unittest.TestCase):
    """Тест контекстного логирования ошибок."""

    def setUp(self) -> None:
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def failing_func():
            raise ConnectionError("Network timeout")

        self.failing_func = failing_func

    def test_error_context(self) -> None:
        """Тест логирования + проброс исключения."""
        with self.assertRaises(ConnectionError):
            self.failing_func()

        logs = self.stream.getvalue()
        self.assertRegex(logs, r"ERROR: failing_func.*ConnectionError")
        self.assertIn("Network timeout", logs)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
    print()
    main()
