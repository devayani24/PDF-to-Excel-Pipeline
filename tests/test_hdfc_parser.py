import pytest
from src.parsers.HDFC_transaction_parser import HDFCTransactionParser

parser = HDFCTransactionParser("tests/artifacts/HDFCSample.pdf")

def test_transform_returns_dataframe():
    
    result = parser.transform()
    assert isinstance(result, result.__class__)
    assert not result.empty


def test_transform_output_columns():
    
    result = parser.transform()
    expected = {"Date", "Transactional details", "Debit", "Credit", "Balance"}
    assert expected.issubset(set(result.columns))


def test_transform_stops_at_statement_summary():
    """STATEMENTSUMMARY rows must never appear in output"""
    
    result = parser.transform()
    assert "STATEMENTSUMMARY" not in result["Transactional details"].values


def test_transform_correct_row_count():
    """5 transactions in dummy HDFC PDF"""
    
    result = parser.transform()
    assert len(result) == 5