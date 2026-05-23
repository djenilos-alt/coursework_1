import json
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)


def save_report(
    filename: str | None = None,
) -> Callable:
    """
    Декоратор для сохранения отчетов в JSON-файл.

    Если filename не передан,
    имя файла создается автоматически.

    :param filename: имя файла
    :return: декоратор
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)

            if filename:
                report_filename = filename
            else:
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

                report_filename = f"{func.__name__}_{current_time}.json"

            report_path = reports_dir / report_filename

            try:
                if isinstance(result, pd.DataFrame):
                    data_to_save = result.to_dict(orient="records")
                else:
                    data_to_save = result

                with open(
                    report_path,
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(
                        data_to_save,
                        file,
                        ensure_ascii=False,
                        indent=4,
                        default=str,
                    )

                logging.info(f"Отчет сохранен: {report_path}")

            except OSError as error:
                logging.error(f"Ошибка сохранения отчета: {error}")

            return result

        return wrapper

    return decorator
