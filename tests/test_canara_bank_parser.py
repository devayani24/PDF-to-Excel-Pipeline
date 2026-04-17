# tests/test_canara_parser.py
import pandas as pd
import pytest
from src.parsers.canara_bank_parser import CanaraBankParser

parser = CanaraBankParser("tests/artifacts/CanaraBankSample.pdf")

def test_transform_returns_dataframe():
    """Full pipeline — PDF in, DataFrame out"""
    
    result = parser.transform()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_transform_output_columns():
    """Canara has different column names from other banks"""
    
    result = parser.transform()
    expected = {"Date", "Transactional details", "Debit", "Credit", "Balance"}
    assert expected.issubset(set(result.columns))


def test_transform_no_closing_balance_row():
    """Parser must stop at 'Closing' — it must not appear in output"""
    
    result = parser.transform()
    assert not result["Transactional details"].str.contains("Closing", na=False).any()