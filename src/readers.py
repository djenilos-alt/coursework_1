import pandas as pd


def read_excel(path: str) -> pd.DataFrame:
    """
    Чтение Excel-файла.
    """

    return pd.read_excel(
        path,
        engine="openpyxl",
    )
