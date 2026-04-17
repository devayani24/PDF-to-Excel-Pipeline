import pandas as pd
from src.components.transformation import DataTransformer
import pytest
from src.exception import CustomException

@pytest.mark.parametrize("data, keyword, expected_index", [

    # Bank 1 - Indian Bank
    (
        ["ACCOUNT DETAILS", "Ending Balance","INR 1,474", "Date Transaction Details Debits Credits Balance", "01 Mar 2026 TRANSFER FROM - INR 1,600.00 INR 7,282,572.44", 
         "12345678912/IMPS/P2A/60","1234567890/","/ABCDEFGHsIoI/GOOGL/BR","ANCH : ATM SERVICE","BRANCH",
         "01 Mar 2026 TRANSFER FROM - INR 392.80 INR 5,282,965.24"],

        r"^\d{2}\s\w{3}\s\d{4}",

        4
    ),

    # Bank 2 - Kotak
    (
        ["Account Statement", "01 Jan 2026 - 21 Feb 2026","MICR 123456789", "# TRANSACTION DATE VALUE DATE TRANSACTION DETAILS CHQ / REF NO. DEBIT/CREDIT(₹) BALANCE(₹)",
        "1 02 Jan 2026 02 Jan 2026 RTGS SBINR1234567899987654 RTGSINW- +7,00,000.00 7,78,358.25","12:26 PM SEKAR SBIN1234567 1234567890",
        "2 02 Jan 2026 02 Jan 2026 MB:SENT RTGS SRI RADHA KRISHNA KKBKR1234567890 -5,00,000.00 2,78,358.25"],

        r"^\d\s\d{2}\s\w{3}\s\d{4}",

        4
    ),

    # Bank 3 - SBI
    (
        ["Statement From : 01-04-2025 to 07-02-2026", " Balance",
        "DEP TFR", "01/04/2025 01/04/2025 UPI/CR/123456789098/R K - - 50,000.00 90,641.68", "UPI/CR/123456789098/R K","YOGA/UTIB/yogabalaji/UPI","1234567890987 AT 08641 WEST","TOWER STREET",
        "WDL TFR","01/04/2025 01/04/2025 UPI/DR/036548276562/Bank - 50,000.00 - 40,641.68"],

       r"^\d{2}/\d{2}/\d{4}",

        3
    )

    
])


def test_find_transaction_start_index(data, keyword, expected_index):
    df = pd.DataFrame({"raw": data})

    transformer = DataTransformer(df, start_index_string=keyword)

    idx = transformer.find_transaction_start_index()

    assert idx == expected_index




def test_transform_empty_dataframe():
    df = pd.DataFrame({"raw": []})

    transformer = DataTransformer(df, start_index_string="Date")

    with pytest.raises(CustomException):
        transformer.transform()

def test_keyword_not_found_raises():
    """keyword exists in parametrize but never tested when completely missing"""
    df = pd.DataFrame({"raw": ["random line", "another line", "nothing useful"]})
    transformer = DataTransformer(df, start_index_string=r"^\d{2}\s\w{3}\s\d{4}")
    with pytest.raises(CustomException):
        transformer.find_transaction_start_index()


def test_transform_removes_header_rows():
    """verify rows ABOVE the start index are actually gone"""
    data = ["BANK HEADER", "Account No: 123", "01 Jan 2024 transaction line"]
    df = pd.DataFrame({"raw": data})
    transformer = DataTransformer(df, start_index_string=r"^\d{2}\s\w{3}\s\d{4}")
    result = transformer.transform()

    assert "BANK HEADER" not in result["raw"].values
    assert "Account No: 123" not in result["raw"].values


def test_transform_resets_index():
    """after trimming, index must start at 0 — not at 2 or 3"""
    data = ["HEADER", "SUBHEADER", "01 Jan 2024 transaction"]
    df = pd.DataFrame({"raw": data})
    transformer = DataTransformer(df, start_index_string=r"^\d{2}\s\w{3}\s\d{4}")
    result = transformer.transform()

    assert result.index[0] == 0


def test_transform_returns_dataframe():
    data = ["HEADER", "01 Jan 2024 transaction"]
    df = pd.DataFrame({"raw": data})
    transformer = DataTransformer(df, start_index_string=r"^\d{2}\s\w{3}\s\d{4}")
    result = transformer.transform()

    assert isinstance(result, pd.DataFrame)