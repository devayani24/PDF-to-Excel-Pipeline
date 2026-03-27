import sys
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List,Tuple
from src.utils import export_dataframe_to_csv,convert_list_to_dataframe

class TransactionParser:

    def __init__(self, txn_df: pd.DataFrame):
        self.txn_df = txn_df

        self.date_pattern = r'(\d{2}\s\w{3}\s\d{4})'
        self.amount_pattern = r'(?:(-)\sINR\s(.+)\sINR\s(.+))|(?:INR\s(.+)\s(-)\sINR\s(.+))'

    # ---------------------------
    # Step 1: Split Rows
    # ---------------------------
    def split_rows(self) -> Tuple[List[str], List[str]]:
        date_rows = []
        txn_details = []
        buffer = []

        for line in self.txn_df["raw"]:

            if "Ending Balance" in line:
                logging.info(f"Stopping at line: {line}")
                break

            if re.search(self.date_pattern, line):
                if buffer:
                    txn_details.append(" ".join(buffer))
                    buffer = []

                date_rows.append(line)
            else:
                buffer.append(line)

        # appending last transaction
        if buffer:
            txn_details.append(" ".join(buffer))

        return date_rows, txn_details

    # ---------------------------
    # Step 2: Extract Fields
    # ---------------------------
    def extract_date(self, line: str) -> str:
        match = re.search(self.date_pattern, line)
        return match.group(1) if match else None

    def extract_amounts(self, line: str) -> Tuple[str, str, str]:
        match = re.search(self.amount_pattern, line)

        if not match:
            return None, None, None

        groups = match.groups()

        if groups[0] is not None:
            return groups[0], groups[1], groups[2]
        else:
            return groups[3], groups[4], groups[5]

    def extract_transaction_details(self, line: str) -> str:
        temp = re.sub(self.date_pattern, "", line)
        temp = re.sub(self.amount_pattern, "", temp)
        return re.sub(r"\s+", " ", temp).strip()

    # ---------------------------
    # Main Method
    # ---------------------------
    def transform(self) -> pd.DataFrame:
        try:
            logging.info("Starting transaction split process")

            date_rows, txn_half_details = self.split_rows()

            export_dataframe_to_csv(
                convert_list_to_dataframe(date_rows, txn_half_details,
                                          columns=["date_row", "txn_half"]),
                "split.csv"
            )

            dates, txn_details, debits, credits, balances = [], [], [], [], []

            for line in date_rows:
                dates.append(self.extract_date(line))

                d, c, b = self.extract_amounts(line)
                debits.append(d)
                credits.append(c)
                balances.append(b)

                txn_details.append(self.extract_transaction_details(line))

            # Combine descriptions
            full_txn = [
                f"{t1} {t2}".strip()
                for t1, t2 in zip(txn_details, txn_half_details)
            ]

            df = convert_list_to_dataframe(
                dates, full_txn, debits, credits, balances,
                columns=["date", "transaction_details", "debit", "credit", "balance"]
            )

            logging.info("Transaction split completed successfully")

            return df

        except Exception as e:
            logging.error("Error in transaction split process")
            raise CustomException(e, sys)

    