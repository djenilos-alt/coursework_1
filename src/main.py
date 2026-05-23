from src.views import main_page
from src.readers import read_excel


if __name__ == "__main__":
    transactions = read_excel(
        "data/operations.xlsx"
    )

    json_response = main_page(
        "2023-05-20 14:30:00",
        transactions,
    )

    print(json_response)
