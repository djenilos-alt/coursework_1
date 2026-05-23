import json
from datetime import datetime
from functools import wraps
from typing import Callable

import pandas as pd


def save_report(filename: str = "report.json") -> Callable:
    """
    Декоратор для сохранения отчета в JSON-файл.

    :param filename: имя файла
    :return: декоратор
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if isinstance(result, pd.DataFrame):
                data_to_save = result.to_dict(orient="records")
            else:
                data_to_save = result

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(
                    data_to_save,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    default=str,
                )

            return result

        return wrapper

    return decorator


@save_report("spending_by_category.json")
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: str | None = None,
) -> pd.DataFrame:
    """
    Возвращает траты по категории
    за последние 3 месяца.

    :param transactions: DataFrame с транзакциями
    :param category: категория
    :param date: дата формата YYYY-MM-DD
    :return: DataFrame
    """

    df = transactions.copy()

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"],
        dayfirst=True,
        errors="coerce",
    )

    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - pd.DateOffset(months=3)

    filtered_df = df[
        (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= end_date)
        & (df["Категория"] == category)
        & (df["Сумма платежа"] < 0)
    ]

    result = filtered_df.groupby(
        "Категория"
    )["Сумма платежа"].sum().abs().reset_index()

    result.columns = ["Категория", "Сумма трат"]

    return result


@save_report("spending_by_weekday.json")
def spending_by_weekday(
    transactions: pd.DataFrame,
    date: str | None = None,
) -> pd.DataFrame:
    """
    Возвращает средние траты
    по дням недели за последние 3 месяца.

    :param transactions: DataFrame с транзакциями
    :param date: дата формата YYYY-MM-DD
    :return: DataFrame
    """

    df = transactions.copy()

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"],
        dayfirst=True,
        errors="coerce",
    )

    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - pd.DateOffset(months=3)

    filtered_df = df[
        (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= end_date)
        & (df["Сумма платежа"] < 0)
    ].copy()

    filtered_df["weekday"] = filtered_df["Дата операции"].dt.day_name()

    result = (
        filtered_df.groupby("weekday")["Сумма платежа"]
        .mean()
        .abs()
        .round(2)
        .reset_index()
    )

    result.columns = [
        "День недели",
        "Средние траты",
    ]

    return result


@save_report("spending_by_workday.json")
def spending_by_workday(
    transactions: pd.DataFrame,
    date: str | None = None,
) -> pd.DataFrame:
    """
    Возвращает средние траты
    в рабочий и выходной день
    за последние 3 месяца.

    :param transactions: DataFrame с транзакциями
    :param date: дата формата YYYY-MM-DD
    :return: DataFrame
    """

    df = transactions.copy()

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"],
        dayfirst=True,
        errors="coerce",
    )

    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - pd.DateOffset(months=3)

    filtered_df = df[
        (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= end_date)
        & (df["Сумма платежа"] < 0)
    ].copy()

    filtered_df["day_type"] = filtered_df["Дата операции"].dt.weekday.apply(
        lambda x: "Выходной" if x >= 5 else "Рабочий"
    )

    result = (
        filtered_df.groupby("day_type")["Сумма платежа"]
        .mean()
        .abs()
        .round(2)
        .reset_index()
    )

    result.columns = [
        "Тип дня",
        "Средние траты",
    ]

    return result
