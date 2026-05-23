import json

import pandas as pd
import pytest

from src.views import events_page, main_page


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.01.2024",
                "02.01.2024",
                "03.01.2024",
                "04.01.2024",
                "05.01.2024",
            ],
            "Номер карты": [
                "*1234",
                "*1234",
                "*5678",
                "*5678",
                "*5678",
            ],
            "Сумма платежа": [
                -1000,
                -500,
                -300,
                2000,
                -150,
            ],
            "Категория": [
                "Супермаркеты",
                "Фастфуд",
                "Топливо",
                "Зарплата",
                "Развлечения",
            ],
            "Описание": [
                "Пятерочка",
                "KFC",
                "Лукойл",
                "Пополнение",
                "Steam",
            ],
        }
    )


def test_main_page_returns_json(
    transactions_df: pd.DataFrame,
) -> None:
    result = main_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert isinstance(data, dict)


def test_main_page_contains_keys(
    transactions_df: pd.DataFrame,
) -> None:
    result = main_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
    assert "currency_rates" in data
    assert "stock_prices" in data


def test_main_page_cards_not_empty(
    transactions_df: pd.DataFrame,
) -> None:
    result = main_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert len(data["cards"]) > 0


def test_main_page_top_transactions_limit(
    transactions_df: pd.DataFrame,
) -> None:
    result = main_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert len(data["top_transactions"]) <= 5


def test_events_page_returns_json(
    transactions_df: pd.DataFrame,
) -> None:
    result = events_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert isinstance(data, dict)


def test_events_page_contains_keys(
    transactions_df: pd.DataFrame,
) -> None:
    result = events_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert "expenses" in data
    assert "income" in data
    assert "currency_rates" in data
    assert "stock_prices" in data


def test_events_page_expenses_structure(
    transactions_df: pd.DataFrame,
) -> None:
    result = events_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert "total_amount" in data["expenses"]
    assert "main" in data["expenses"]


def test_events_page_income_structure(
    transactions_df: pd.DataFrame,
) -> None:
    result = events_page(
        "2024-01-05 12:00:00",
        transactions_df,
    )

    data = json.loads(result)

    assert "total_amount" in data["income"]
    assert "main" in data["income"]
