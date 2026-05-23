import pandas as pd
import pytest

from src.reports import (spending_by_category, spending_by_weekday,
                         spending_by_workday)


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.01.2024",
                "02.01.2024",
                "06.01.2024",
            ],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Фастфуд",
            ],
            "Сумма платежа": [
                -1000,
                -500,
                -300,
            ],
        }
    )


def test_spending_by_category(
    transactions_df: pd.DataFrame,
) -> None:
    result = spending_by_category(
        transactions_df,
        "Супермаркеты",
        "2024-03-01",
    )

    assert not result.empty
    assert result.iloc[0]["Сумма трат"] == 1500


def test_spending_by_weekday(
    transactions_df: pd.DataFrame,
) -> None:
    result = spending_by_weekday(
        transactions_df,
        "2024-03-01",
    )

    assert not result.empty
    assert "Средние траты" in result.columns


def test_spending_by_workday(
    transactions_df: pd.DataFrame,
) -> None:
    result = spending_by_workday(
        transactions_df,
        "2024-03-01",
    )

    assert not result.empty
    assert "Тип дня" in result.columns
