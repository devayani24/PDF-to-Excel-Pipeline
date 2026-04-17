# test_ingestion.py
import pandas as pd
import pytest
from src.components.ingestion import PDFPlumberReader
from src.exception import CustomException

PLAIN_PDF = "tests/artifacts/sample_bank.pdf"
ENCRYPTED_PDF = "tests/artifacts/sample_bank_encrypted.pdf"
TEST_PASSWORD = "test1234" 

def test_extract_text_returns_list():
    reader = PDFPlumberReader()
    rows = reader.extract_text_from_pdf(PLAIN_PDF, password=None)
    assert isinstance(rows, list)
    assert len(rows) > 0

def test_encrypted_pdf_correct_password():
    reader = PDFPlumberReader()
    rows = reader.extract_text_from_pdf(ENCRYPTED_PDF, password=TEST_PASSWORD)
    assert isinstance(rows, list)
    assert len(rows) > 0

def test_encrypted_pdf_wrong_password():
    reader = PDFPlumberReader()
    with pytest.raises(CustomException):
        reader.extract_text_from_pdf(ENCRYPTED_PDF, password="wrong_password")
        

def test_file_not_found_raises():
    reader = PDFPlumberReader()
    with pytest.raises(CustomException):
        reader.extract_text_from_pdf("tests/artifacts/nonexistent.pdf", password=None)

def test_to_dataframe_returns_correct_shape():
    reader = PDFPlumberReader()
    df = reader.to_dataframe(PLAIN_PDF)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "raw" in df.columns
    assert df.shape[1] == 1  # ← should have exactly 1 column