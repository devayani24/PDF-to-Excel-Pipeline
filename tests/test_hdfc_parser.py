# tests/test_hdfc_parser.py
import pytest
from src.parsers.HDFC_parser import HDFCTransactionParser

def test_transform_output():
    result = HDFCTransactionParser("tests/artifacts/HDFCSample.pdf").transform()
    assert {"Date", "Transactional details", "Debit", "Credit", "Balance"}.issubset(set(result.columns))
    assert len(result) == 5

def test_stops_at_summary():
    result = HDFCTransactionParser("tests/artifacts/HDFCSample.pdf").transform()
    assert "STATEMENTSUMMARY" not in result["Transactional details"].values