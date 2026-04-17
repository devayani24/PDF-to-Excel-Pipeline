import pandas as pd
import pytest
from src.parsers.KVB_transaction_parser import KVBParser

parser = KVBParser("tests/artifacts/KVBSample.pdf")

def test_transform_returns_dataframe():
    
    result = parser.transform()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_transform_output_columns():
    
    result = parser.transform()
    expected = {"Date", "Transactional details", "Debit", "Credit", "Balance"}
    assert expected.issubset(set(result.columns))


def test_transform_correct_row_count():
    """6 transactions in dummy PDF"""
    
    result = parser.transform()
    assert len(result) == 6