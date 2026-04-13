import sys
import pandas as pd
import re
from dataclasses import dataclass, field
from typing import List,Tuple

from src.exception import CustomException
from src.logger import logging

from src.parsers.base_transaction_parser import BaseTransactionParser

@dataclass
class KotakConfig():
    date_pattern: str = r'(\d{2}\s\w{3}\s\d{4})'
    amt_pattern: str = r'(\s[-+].+)'
    remove_patterns: list = field(default_factory=lambda: [r'\d{2}:\d{2}\s[AP]M',r'\s[0-9]+\s*',r'([A-Z]+)-[0-9]*', r'KKBK[HR][0-9]+'])

  
    

class KotakTransactionParser(BaseTransactionParser):
    def __init__(self,config:KotakConfig, txn_df: pd.DataFrame):
        super().__init__(txn_df)
        self.start_txn_pattern = r'(^\d*\s\d{2}\s\w{3}\s\d{4})'
        self.config = config

    
    
    
    # Override base method
    def extract_amounts(self, line: str) -> Tuple[str, str, str]:

        match = re.search(self.config.amt_pattern, line)
        
        if not match:
                return None, None, None
            
        credit_debit, balance = match.group().strip().split(" ")
        
        if '+' in credit_debit:
            credit = credit_debit.replace('+',"")
            debit = None
        else:
            debit = credit_debit.replace('-',"")
            credit = None
    
        return debit,credit,balance

    def extract_transaction_details(self, line: str) -> str:
        temp = re.sub(r'^\d* ',"",line)
        temp = re.sub(self.config.date_pattern, "", temp)
        temp = re.sub(self.config.amt_pattern, "", temp)
        
        for i in self.config.remove_patterns:
            temp = re.sub(i, "", temp)
        
        return temp.strip()
    
    def combine_transaction_details(self,txn_details_from_date_row,splitted_txn_half_details): 

        splitted_txn_half_details = [ self.extract_transaction_details(line) for line in splitted_txn_half_details]
        logging.info("Cleaned splitted_txn_half_details by filtering some patterns")
        
        try:
            if len(splitted_txn_half_details) == len(txn_details_from_date_row):
                full_txn = [
                        f"{t1} {t2}".strip()
                        for t1, t2 in zip(txn_details_from_date_row, splitted_txn_half_details)
                    ]
                return full_txn
            else:
                raise ValueError(f"List lengths mismatch while combining two transactional details")
        
        except Exception as e:
            logging.error("Error in combine_full_transaction process")
            raise CustomException(e, sys)



