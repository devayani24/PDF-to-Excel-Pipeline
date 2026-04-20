# tests/test_sbi_parser.py
import pandas as pd
import pytest
from src.parsers.SBI_parser import SBITransactionParser

@pytest.fixture
def parser():
    return SBITransactionParser(pd.DataFrame({"raw": []}))

@pytest.fixture
def sbi_df():
    lines = [
        "01/04/2025 01/04/2025 UPI/CR/123456789098 - 50,000.00 90,641.68",
        "UPI/CR/123456789098/R K",
        "01/04/2025 01/04/2025 UPI/DR/036548276562/Bank 50,000.00 - 40,641.68",
        "Statement Summary",
    ]
    return pd.DataFrame({"raw": lines})

def test_extract_date(parser):
    assert parser.extract_date("01/04/2025 UPI/CR - 50,000.00 90,641.68") == "01/04/2025"

def test_extract_amounts(parser):
    debit, credit, balance = parser.extract_amounts("01/04/2025 UPI/CR - 50,000.00 90,641.68")
    assert balance == "90,641.68"

def test_transform_output(sbi_df):
    result = SBITransactionParser(sbi_df).transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 2