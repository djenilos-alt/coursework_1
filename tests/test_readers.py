import pandas as pd

from src.readers import read_excel


def test_read_excel(tmp_path) -> None:
    file_path = tmp_path / "test.xlsx"

    df = pd.DataFrame(
        {
            "col1": [1, 2],
            "col2": [3, 4],
        }
    )

    df.to_excel(
        file_path,
        index=False,
    )

    result = read_excel(str(file_path))

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
