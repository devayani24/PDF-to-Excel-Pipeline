import sys
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List,Tuple

from src.parsers.base_transaction_parser import BaseTransactionParser
from src.utils import export_dataframe_to_csv,convert_list_to_dataframe


class SBITransactionParser(BaseTransactionParser):

    def __init__(self, txn_df: pd.DataFrame):
        super().__init__(txn_df)
        self.date_patterns = r'(\d{2}/\d{2}/\d{4})'
        self.start_txn_pattern = self.date_patterns
       

    def extract_date(self, line: str) -> str:
        match = re.search(self.date_patterns, line)
        return match.group(1) if match else None

    def extract_amounts(self, line: str) -> Tuple[str, str, str]:
        split_line = line.split(" ")
        debit = split_line[-3]
        credit = split_line[-2]
        balance = split_line[-1]
        return debit,credit,balance

    def extract_transaction_details(self, line: str) -> str:
        temp = re.sub(self.date_patterns, "", line)
        temp =  " ".join(temp.split(" ")[:-4]).strip()
        
        return  temp
    


    