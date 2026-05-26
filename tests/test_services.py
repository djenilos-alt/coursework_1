import pandas as pd
import pytest

from src.services import (
    cashback_categories,
    investment_bank,
    search_by_phone,
    search_transfers,
    simple_search,
)


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

