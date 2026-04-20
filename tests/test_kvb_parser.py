# tests/test_kvb_parser.py
import pytest
from src.parsers.KVB_parser import KVBParser

def test_transform_output():
    result = KVBParser("tests/artifacts/KVBSample.pdf").transform()
    assert {"Date", "Transactional details", "Debit", "Credit", "Balance"}.issubset(set(result.columns))
    assert len(result) == 6