# tests/test_base_transaction_parser.py
import pandas as pd
import pytest
from src.parsers.base_transaction_parser import BaseTransactionParser


@pytest.fixture
def parser():
    return BaseTransactionParser(pd.DataFrame({"raw": []}))


@pytest.fixture
def indian_bank_df():
    lines = [
        "01 Mar 2026 TRANSFER FROM - INR 1,600.00 INR 7,282,572.44",
        "12345678912/IMPS/P2A/60",
        "02 Mar 2026 SALARY CREDIT INR 85,000.00 - INR 7,367,572.44",
        "SALARY MARCH 2026",
        "03 Mar 2026 ATM WITHDRAWAL - INR 5,000.00 INR 7,362,572.44",
        "Statement Summary",
        "Total Debits: 6,600.00",
    ]
    return pd.DataFrame({"raw": lines})


# One test per method — covers the core behaviour
def test_extract_date(parser):
    assert parser.extract_date("01 Mar 2026 TRANSFER FROM - INR 1,600.00") == "01 Mar 2026"

def test_extract_date_returns_none_for_continuation(parser):
    assert parser.extract_date("12345678912/IMPS/P2A/60") is None

def test_extract_amounts_debit(parser):
    sign, amount, balance = parser.extract_amounts("01 Mar 2026 - INR 1,600.00 INR 7,282,572.44")
    assert sign == "-"
    assert amount == "1,600.00"
    assert balance == "7,282,572.44"

def test_extract_amounts_returns_none_for_continuation(parser):
    assert parser.extract_amounts("12345678912/IMPS/P2A/60") == (None, None, None)

def test_split_transactions_length_match(indian_bank_df):
    parser = BaseTransactionParser(indian_bank_df)
    date_rows, txn_details = parser.split_transactions()
    assert len(date_rows) == len(txn_details)

def test_split_transactions_stops_at_summary(indian_bank_df):
    parser = BaseTransactionParser(indian_bank_df)
    _, txn_details = parser.split_transactions()
    assert not any("Total Debits" in (d or "") for d in txn_details)

def test_transform_output_shape(indian_bank_df):
    parser = BaseTransactionParser(indian_bank_df)
    result = parser.transform()
    assert set(result.columns) == {"date", "transaction_details", "debit", "credit", "balance"}
    assert len(result) == 3
    # assert result["date"].tolist() == ["01 Mar 2026","02 Mar 2026","03 Mar 2026"]
    # assert result["transaction_details"].tolist() == ["TRANSFER FROM 12345678912/IMPS/P2A/60","SALARY CREDIT SALARY MARCH 2026","ATM WITHDRAWAL None"]
    # assert result["debit"].tolist() == ["-","85,000.00","-"]
    # assert result["credit"].tolist() == ["1,600.00","-","5,000.00"]
    # assert result["balance"].tolist() == ["7,282,572.44","7,367,572.44","7,362,572.44"]