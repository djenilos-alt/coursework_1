import json
import math

from typing import Any

import pandas as pd

PHONE_PATTERN = (
    r"(\+7|8)\s?" r"\(?\d{3}\)?" r"[\s-]?\d{3}" r"[\s-]?\d{2}" r"[\s-]?\d{2}"
)

TRANSFER_PATTERN = r"[А-ЯA-Z][а-яa-z]+\s[А-ЯA-Z]\."


def simple_search(data: pd.DataFrame, query: str) -> str:
    """
    Поиск транзакций по категории или описанию.

    Поиск:
    - нечувствителен к регистру
    - работает по подстроке

    :param data: DataFrame с транзакциями
    :param query: поисковая строка
    :return: JSON-строка
    """

    mask = data["Описание"].astype(str).str.contains(
        query,
        case=False,
        na=False,
    ) | data["Категория"].astype(str).str.contains(
        query,
        case=False,
        na=False,
    )

    result = data[mask]

    return result.to_json(
        orient="records",
        force_ascii=False,
        indent=4,
    )


def search_by_phone(data: pd.DataFrame) -> str:
    """
    Поиск транзакций с телефонными номерами.

    Поддерживаются форматы:
    +7 (900) 000-00-00
    89000000000

    :param data: DataFrame с транзакциями
    :return: JSON-строка
    """

    mask = (
        data["Описание"]
        .astype(str)
        .str.contains(
            PHONE_PATTERN,
            regex=True,
            na=False,
        )
    )

    result = data[mask]

    return result.to_json(
        orient="records",
        force_ascii=False,
        indent=4,
    )


def search_transfers(data: pd.DataFrame) -> str:
    """
    Поиск переводов физическим лицам.

    Условия:
    - категория = "Переводы"
    - описание содержит имя и первую букву фамилии

    Примеры:
    Валерий А.
    Сергей З.

    :param data: DataFrame с транзакциями
    :return: JSON-строка
    """

    category_mask = (
        data["Категория"]
        .astype(str)
        .str.contains(
            "Переводы",
            case=False,
            na=False,
        )
    )

    description_mask = (
        data["Описание"]
        .astype(str)
        .str.contains(
            TRANSFER_PATTERN,
            regex=True,
            na=False,
        )
    )

    result = data[category_mask & description_mask]

    return result.to_json(
        orient="records",
        force_ascii=False,
        indent=4,
    )


def investment_bank(
    month: str,
    transactions: list[dict[str, Any]],
    limit: int,
) -> float:
    """
    Рассчитывает сумму,
    которую можно было бы отложить
    в Инвесткопилку.

    :param month: месяц формата YYYY-MM
    :param transactions: список транзакций
    :param limit: шаг округления
    :return: сумма накоплений
    """

    total_saved = 0.0

    for transaction in transactions:
        operation_date = transaction.get("Дата операции")
        amount = transaction.get("Сумма операции", 0)

        if not operation_date:
            continue

        transaction_month = operation_date[:7]

        if transaction_month != month:
            continue

        if amount <= 0:
            continue

        rounded_amount = math.ceil(amount / limit) * limit

        saved_amount = rounded_amount - amount

        total_saved += saved_amount

    return round(total_saved, 2)


def cashback_categories(
    data: pd.DataFrame,
    year: int,
    month: int,
) -> str:
    """
    Анализ категорий повышенного кешбэка.

    Кешбэк:
    1 рубль на каждые 100 рублей расходов.

    :param data: DataFrame с транзакциями
    :param year: год
    :param month: месяц
    :return: JSON-строка
    """

    df = data.copy()

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"],
        dayfirst=True,
        errors="coerce",
    )

    filtered_df = df[
        (df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month)
    ]

    expenses_df = filtered_df[filtered_df["Сумма платежа"] < 0].copy()

    expenses_df["cashback"] = expenses_df["Сумма платежа"].abs() / 100

    grouped = (
        expenses_df.groupby("Категория")["cashback"].sum().sort_values(ascending=False)
    )

    result = {category: round(value, 2) for category, value in grouped.items()}

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=4,
    )
