import pandas as pd
import pytest
from src.parsers.SBI_transaction_parser import SBITransactionParser


@pytest.fixture
def parser():
    return SBITransactionParser(pd.DataFrame({"raw": []}))


def test_extract_date(parser):
    """SBI uses DD/MM/YYYY format — different from base"""
    line = "01/04/2025 01/04/2025 UPI/CR/123456789098 - - 50,000.00 90,641.68"
    assert parser.extract_date(line) == "01/04/2025"


def test_extract_date_returns_none_for_continuation(parser):
    line = "UPI/CR/123456789098/R K"
    assert parser.extract_date(line) is None


def test_extract_amounts(parser):
    """SBI has fixed positions — last 3 items are debit, credit, balance"""
    line = "01/04/2025 01/04/2025 UPI/CR/123456789098 - - 50,000.00 90,641.68"
    debit, credit, balance = parser.extract_amounts(line)
    assert balance == "90,641.68"
    assert credit == "50,000.00"
    assert debit == "-"


def test_extract_transaction_details(parser):
    """Description must have dates and last 4 items stripped"""
    line = "01/04/2025 01/04/2025 UPI/CR/123456789098 - - 50,000.00 90,641.68"
    result = parser.extract_transaction_details(line)
    assert "01/04/2025" not in result
    assert "90,641.68" not in result
    assert "UPI/CR/123456789098" in result