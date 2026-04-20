# tests/test_kotak_parser.py
import pandas as pd
import pytest
from src.parsers.kotak_parser import KotakTransactionParser

@pytest.fixture
def parser():
    return KotakTransactionParser(pd.DataFrame({"raw": []}))

@pytest.fixture
def kotak_df():
    lines = [
        "1 02 Jan 2026 02 Jan 2026 RTGS SBINR12345 +7,00,000.00 7,78,358.25",
        "12:26 PM SEKAR SBIN1234567",
        "2 02 Jan 2026 02 Jan 2026 MB:SENT KKBKR1234567890 -5,00,000.00 2,78,358.25",
        "12:30 PM AJ SBIN1234567",
        "Statement Summary",
    ]
    return pd.DataFrame({"raw": lines})

def test_extract_amounts_credit(parser):
    _, credit, _ = parser.extract_amounts("1 02 Jan 2026 RTGS +7,00,000.00 7,78,358.25")
    assert credit == "7,00,000.00"

def test_extract_amounts_debit(parser):
    debit, _, _ = parser.extract_amounts("2 02 Jan 2026 MB:SENT -5,00,000.00 2,78,358.25")
    assert debit == "5,00,000.00"

def test_extract_details_removes_noise(parser):
    result = parser.extract_transaction_details("2 02 Jan 2026 MB:SENT KKBKR1234567890 12:45 PM -5,00,000.00 2,78,358.25")
    assert "KKBKR1234567890" not in result
    assert "12:45 PM" not in result

def test_transform_output(kotak_df):
    result = KotakTransactionParser(kotak_df).transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 2