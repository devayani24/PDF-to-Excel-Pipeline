# tests/test_base_coordinate_parser.py
import pytest
from src.parsers.base_coordinate_parser import BaseCoordinateParser
from src.parsers.canara_bank_parser import CanaraBankParser
from src.parsers.HDFC_parser import HDFCTransactionParser

def test_base_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseCoordinateParser("data/sample.pdf")

def test_should_stop(  ):
    parser = CanaraBankParser("tests/artifacts/CanaraBankSample.pdf")
    assert parser._should_stop("Closing Balance") is True
    assert parser._should_stop("Normal line") is False

def test_should_break():
    parser = HDFCTransactionParser("tests/artifacts/HDFCSample.pdf")
    assert parser._should_break("HDFCBANKLIMITED") is True
    assert parser._should_break("Normal line") is False