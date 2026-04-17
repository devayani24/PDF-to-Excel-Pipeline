# tests/test_base_processor.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.processors.base_processor import BaseProcessor
from src.exception import CustomException


# ─── Test 1: Full pipeline returns a DataFrame ────────────────────────────────

def test_transform_returns_dataframe():
    """
    Uses the sample PDF we created earlier.
    Checks the full pipeline runs without crashing.
    """
    processor = BaseProcessor("tests/artifacts/sample_bank.pdf", password=None)
    result = processor.transform()

    assert isinstance(result, pd.DataFrame)
    assert not result.empty


# ─── Test 2: Invalid file raises CustomException ──────────────────────────────

def test_transform_raises_on_invalid_file():
    """
    If file doesn't exist, must raise CustomException.
    Not crash with a random Python error.
    """
    processor = BaseProcessor("tests/artifacts/nonexistent.pdf", password=None)

    with pytest.raises(CustomException):
        processor.transform()