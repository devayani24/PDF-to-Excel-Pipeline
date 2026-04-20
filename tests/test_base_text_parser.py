# tests/test_base_text_parser.py
import pandas as pd
import pytest
from src.parsers.base_text_parser import BaseTextParser, BaseTextParserConfig


class ConcreteTextParser(BaseTextParser):
    def _get_config(self):
        return BaseTextParserConfig(
            date_patterns  = r'(\d{2}\s\w{3}\s\d{4})',
            amount_pattern = r'(?:(-)\sINR\s(.+)\sINR\s(.+))|(?:INR\s(.+)\s(-)\sINR\s(.+))',
            stop_markers   = ("Ending Balance", "Statement Summary")
        )

@pytest.fixture
def parser():
    lines = [
        "01 Mar 2026 TRANSFER FROM - INR 1,600.00 INR 7,282,572.44",
        "12345678912/IMPS/P2A/60",
        "02 Mar 2026 SALARY CREDIT INR 85,000.00 - INR 7,367,572.44",
        "SALARY MARCH 2026",
        "Statement Summary",
    ]
    return ConcreteTextParser(pd.DataFrame({"raw": lines}))

def test_base_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseTextParser(pd.DataFrame({"raw": []}))

def test_split_transactions_same_length(parser):
    date_rows, txn_details = parser.split_transactions()
    assert len(date_rows) == len(txn_details)

def test_extract_date(parser):
    assert parser.extract_date("01 Mar 2026 TRANSFER - INR 1,600.00 INR 7,282,572.44") == "01 Mar 2026"

def test_extract_amounts_debit(parser):
    sign, amount, balance = parser.extract_amounts("01 Mar 2026 - INR 1,600.00 INR 7,282,572.44")
    assert sign == "-"
    assert amount == "1,600.00"

def test_transform_output(parser):
    result = parser.transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 2