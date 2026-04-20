# tests/test_indian_bank_parser.py
import pandas as pd
import pytest
from src.parsers.indian_bank_parser import IndianBankParser

@pytest.fixture
def indian_bank_df():
    lines = [
        "01 Mar 2026 TRANSFER FROM - INR 1,600.00 INR 7,282,572.44",
        "12345678912/IMPS/P2A/60",
        "02 Mar 2026 SALARY CREDIT INR 85,000.00 - INR 7,367,572.44",
        "Ending Balance",
    ]
    return pd.DataFrame({"raw": lines})

def test_transform_output(indian_bank_df):
    result = IndianBankParser(indian_bank_df).transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 2