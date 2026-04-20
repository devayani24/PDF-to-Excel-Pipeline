# tests/test_canara_parser.py
import pytest
from src.parsers.canara_bank_parser import CanaraBankParser

def test_transform_output():
    result = CanaraBankParser("tests/artifacts/CanaraBankSample.pdf").transform()
    assert {"Date", "Transactional details", "Debit", "Credit", "Balance"}.issubset(set(result.columns))
    assert not result.empty

def test_fix_particulars_no_bleed():
    parser = CanaraBankParser("tests/artifacts/CanaraBankSample.pdf")
    result = parser._fix_particulars([
        "TRANSACTION ONE Chq: 111111 111111 TRANSACTION TWO Chq: 222222",
    ])
    # First transaction should end at chq number
    assert "111111" in result[0]
    assert result[0].endswith("111111")