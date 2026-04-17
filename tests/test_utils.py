import pytest
import pandas as pd
from src.utils import convert_list_to_dataframe, dataframe_validation, export_dataframe_to_csv
from src.exception import CustomException


# ─── dataframe_validation() ──────────────────────────────────────────────────

def test_validation_passes_equal_lengths():
    """Should not raise when all lists are same length"""
    dataframe_validation([1, 2, 3], [4, 5, 6], columns=["a", "b"])


def test_validation_raises_on_length_mismatch():
    """Must raise when lists are different lengths"""
    with pytest.raises(CustomException):
        dataframe_validation([1, 2, 3], [4, 5], columns=["a", "b"])


def test_validation_raises_on_empty_input():
    """Must raise when no data provided"""
    with pytest.raises(CustomException):
        dataframe_validation(columns=["a", "b"])


# ─── convert_list_to_dataframe() ─────────────────────────────────────────────

def test_convert_creates_correct_columns():
    result = convert_list_to_dataframe(
        ["01 Jan 2024", "02 Jan 2024"],
        ["UPI PAYMENT", "SALARY"],
        ["450.00", None],
        [None, "85000.00"],
        ["49550.00", "134550.00"],
        columns=["date", "details", "debit", "credit", "balance"]
    )
    assert list(result.columns) == ["date", "details", "debit", "credit", "balance"]


def test_convert_correct_row_count():
    result = convert_list_to_dataframe(
        ["01 Jan 2024", "02 Jan 2024"],
        ["UPI", "SALARY"],
        columns=["date", "details"]
    )
    assert len(result) == 2


def test_convert_raises_on_column_mismatch():
    """3 lists but only 2 column names — must raise"""
    with pytest.raises(CustomException):
        convert_list_to_dataframe(
            [1, 2], [3, 4], [5, 6],
            columns=["a", "b"]
        )


# ─── export_dataframe_to_csv() ───────────────────────────────────────────────

def test_export_creates_file(tmp_path):
    """tmp_path is a pytest built-in — gives a clean temp folder"""
    df = pd.DataFrame({"date": ["01 Jan 2024"], "amount": [450.00]})
    path = export_dataframe_to_csv(df, "test_output.csv", str(tmp_path))

    assert path is not None
    assert path.endswith(".csv")


def test_export_file_has_correct_content(tmp_path):
    df = pd.DataFrame({"date": ["01 Jan 2024"], "amount": [450.00]})
    path = export_dataframe_to_csv(df, "test_output.csv", str(tmp_path))

    result = pd.read_csv(path)
    assert list(result.columns) == ["date", "amount"]
    assert len(result) == 1