import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")

EXCHANGE_URL = "https://v6.exchangerate-api.com/v6"
STOCK_URL = "https://finnhub.io/api/v1/quote"


def get_currency_rates(
    currencies: list[str],
) -> list[dict[str, Any]]:
    """
    Получение курсов валют.

    :param currencies: список валют
    :return: список словарей
    """

    result: list[dict[str, Any]] = []

    if not EXCHANGE_API_KEY:
        logging.error("Отсутствует EXCHANGE_API_KEY")
        return result

    try:
        response = requests.get(
            f"{EXCHANGE_URL}/{EXCHANGE_API_KEY}/latest/RUB",
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        conversion_rates = data.get(
            "conversion_rates",
            {},
        )

        for currency in currencies:
            rate = conversion_rates.get(currency)

            if rate:
                result.append(
                    {
                        "currency": currency,
                        "rate": round(1 / rate, 2),
                    }
                )

    except requests.RequestException as error:
        logging.error(f"Ошибка получения курсов валют: {error}")

    return result


def get_stock_prices(
    stocks: list[str],
) -> list[dict[str, Any]]:
    """
    Получение стоимости акций.

    :param stocks: список тикеров
    :return: список словарей
    """

    result: list[dict[str, Any]] = []

    if not STOCK_API_KEY:
        logging.error("Отсутствует STOCK_API_KEY")
        return result

    for stock in stocks:
        try:
            response = requests.get(
                STOCK_URL,
                params={
                    "symbol": stock,
                    "token": STOCK_API_KEY,
                },
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            current_price = data.get("c")

            if current_price:
                result.append(
                    {
                        "stock": stock,
                        "price": round(float(current_price), 2),
                    }
                )

        except requests.RequestException as error:
            logging.error(f"Ошибка получения акции " f"{stock}: {error}")

    return result
