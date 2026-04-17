# tests/test_kotak_parser.py
import pandas as pd
import pytest
from src.parsers.kotak_transaction_parser import KotakTransactionParser, KotakConfig


@pytest.fixture
def parser():
    config = KotakConfig()
    return KotakTransactionParser(config, pd.DataFrame({"raw": []}))


@pytest.fixture
def kotak_df():
    lines = [
        "1 02 Jan 2026 02 Jan 2026 RTGS SBINR12345 RTGSINW- +7,00,000.00 7,78,358.25",
        "12:26 PM SEKAR SBIN1234567 1234567890",
        "2 02 Jan 2026 02 Jan 2026 MB:SENT RTGS KKBKR1234567890 -5,00,000.00 2,78,358.25",
        "12:45 PM RADHA KKBK1234567",
        "Statement Summary",
    ]
    return pd.DataFrame({"raw": lines})


def test_extract_amounts_credit(parser):
    """+ means credit — unique to Kotak"""
    line = "1 02 Jan 2026 RTGS +7,00,000.00 7,78,358.25"
    debit, credit, balance = parser.extract_amounts(line)
    assert debit is None
    assert credit == "7,00,000.00"


def test_extract_amounts_debit(parser):
    """- means debit — unique to Kotak"""
    line = "2 02 Jan 2026 MB:SENT -5,00,000.00 2,78,358.25"
    debit, credit, balance = parser.extract_amounts(line)
    assert debit == "5,00,000.00"
    assert credit is None


def test_extract_transaction_details_removes_noise(parser):
    """Serial number, timestamp, KKBK ref must all be stripped"""
    line = "2 02 Jan 2026 02 Jan 2026 MB:SENT KKBKR1234567890 12:45 PM -5,00,000.00 2,78,358.25"
    result = parser.extract_transaction_details(line)
    assert not result.startswith("2")
    assert "12:45 PM" not in result
    assert "KKBKR1234567890" not in result


def test_transform_output_shape(kotak_df):
    config = KotakConfig()
    parser = KotakTransactionParser(config, kotak_df)
    result = parser.transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 2