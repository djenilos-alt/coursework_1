import logging
from datetime import datetime

import pandas as pd
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка транзакций из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        raise


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: list) -> list:
    """Получение курсов валют через API."""
    rates = []
    for currency in currencies:
        try:
            # Пример использования API (замените на реальный)
            response = requests.get(
                f"https://api.exchangerate-api.com/v4/latest/{currency}"
            )
            data = response.json()
            rates.append(
                {"currency": currency, "rate": round(data["rates"]["RUB"], 2)}
            )
        except Exception as e:
            logger.warning(f"Не удалось получить курс для {currency}: {e}")
            rates.append({"currency": currency, "rate": 0.0})
    return rates


def get_stock_prices(stocks: list) -> list:
    """Получение цен на акции через API."""
    prices = []
    for stock in stocks:
        try:
            # Пример использования API (замените на реальный)
            response = requests.get(
                f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey=YOUR_API_KEY"
            )
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            prices.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            logger.warning(f"Не удалось получить цену для {stock}: {e}")
            prices.append({"stock": stock, "price": 0.0})
    return prices
