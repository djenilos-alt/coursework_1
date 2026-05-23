import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# =========================
# BASE PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
TESTS_DIR = BASE_DIR / "tests"


# =========================
# FILE PATHS
# =========================

DATA_FILE = DATA_DIR / "operations.xl"

LOG_FILE = LOGS_DIR / "app.log"

USER_SETTINGS_FILE = BASE_DIR / "user_settings.json"


# =========================
# API SETTINGS
# =========================

EXCHANGE_API_KEY = os.getenv(
    "EXCHANGE_API_KEY",
    "",
)

STOCK_API_KEY = os.getenv(
    "STOCK_API_KEY",
    "",
)


# =========================
# API URLS
# =========================

EXCHANGE_API_URL = "https://v6.exchangerate-api.com/v6"

STOCK_API_URL = "https://finnhub.io/api/v1/quote"


# =========================
# REPORT SETTINGS
# =========================

TOP_TRANSACTIONS_COUNT = 5

TOP_CATEGORIES_COUNT = 7

MONTHS_FOR_REPORTS = 3


# =========================
# DATE SETTINGS
# =========================

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

OUTPUT_DATE_FORMAT = "%d.%m.%Y"


# =========================
# INVESTMENT BANK
# =========================

INVESTMENT_LIMITS = [10, 50, 100]


# =========================
# SEARCH REGEX
# =========================

PHONE_PATTERN = (
    r"(\+7|8)\s?" r"\(?\d{3}\)?" r"[\s-]?\d{3}" r"[\s-]?\d{2}" r"[\s-]?\d{2}"
)

TRANSFER_PATTERN = r"[А-ЯA-Z][а-яa-z]+\s[А-ЯA-Z]\."


# =========================
# LOGGING SETTINGS
# =========================

LOGGING_LEVEL = "INFO"

LOGGING_FORMAT = "%(asctime)s " "%(levelname)s " "%(message)s"


# =========================
# CREATE DIRECTORIES
# =========================

LOGS_DIR.mkdir(exist_ok=True)

REPORTS_DIR.mkdir(exist_ok=True)
