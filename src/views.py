import json
from datetime import datetime

import pandas as pd

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import get_greeting


def main_page(
    date_time: str,
    transactions: pd.DataFrame,
) -> str:
    """
    Главная страница.
    """

    dt = datetime.strptime(
        date_time,
        "%Y-%m-%d %H:%M:%S",
    )

    greeting = get_greeting(dt)

    cards = []

    grouped_cards = transactions.groupby("Номер карты")["Сумма платежа"].sum()

    for card, amount in grouped_cards.items():
        cards.append(
            {
                "last_digits": str(card)[-4:],
                "total_spent": round(abs(amount), 2),
                "cashback": round(
                    abs(amount) / 100,
                    2,
                ),
            }
        )

    top_transactions_df = transactions.sort_values(
        by="Сумма платежа",
        ascending=False,
    ).head(5)

    top_transactions = []

    for _, row in top_transactions_df.iterrows():
        top_transactions.append(
            {
                "date": row["Дата операции"],
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": get_currency_rates(["USD", "EUR"]),
        "stock_prices": get_stock_prices(
            [
                "AAPL",
                "AMZN",
                "GOOGL",
            ]
        ),
    }

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=4,
    )


def events_page(
    date_time: str,
    transactions: pd.DataFrame,
) -> str:
    """
    Страница событий.
    """

    expenses_df = transactions[transactions["Сумма платежа"] < 0]

    income_df = transactions[transactions["Сумма платежа"] > 0]

    expenses_total = int(abs(expenses_df["Сумма платежа"].sum()))

    income_total = int(income_df["Сумма платежа"].sum())

    expenses_main = []

    grouped_expenses = (
        expenses_df.groupby("Категория")["Сумма платежа"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    for category, amount in grouped_expenses.items():
        expenses_main.append(
            {
                "category": category,
                "amount": int(amount),
            }
        )

    income_main = []

    grouped_income = (
        income_df.groupby("Категория")["Сумма платежа"]
        .sum()
        .sort_values(ascending=False)
    )

    for category, amount in grouped_income.items():
        income_main.append(
            {
                "category": category,
                "amount": int(amount),
            }
        )

    response = {
        "expenses": {
            "total_amount": expenses_total,
            "main": expenses_main,
        },
        "income": {
            "total_amount": income_total,
            "main": income_main,
        },
        "currency_rates": get_currency_rates(["USD", "EUR"]),
        "stock_prices": get_stock_prices(
            [
                "AAPL",
                "AMZN",
                "GOOGL",
            ]
        ),
    }

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=4,
    )
