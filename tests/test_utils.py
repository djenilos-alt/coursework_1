from datetime import datetime

from src.utils import get_greeting


def test_get_greeting_morning() -> None:
    dt = datetime(2024, 1, 1, 8)

    assert get_greeting(dt) == ("Доброе утро")


def test_get_greeting_day() -> None:
    dt = datetime(2024, 1, 1, 14)

    assert get_greeting(dt) == ("Добрый день")


def test_get_greeting_evening() -> None:
    dt = datetime(2024, 1, 1, 20)

    assert get_greeting(dt) == ("Добрый вечер")


def test_get_greeting_night() -> None:
    dt = datetime(2024, 1, 1, 2)

    assert get_greeting(dt) == ("Доброй ночи")
