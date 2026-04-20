from src.processors.base_text_processor import BaseTextProcessor
from src.parsers.SBI_parser import SBITransactionParser


class SBIProcessor(BaseTextProcessor):

    def get_parser(self, txn_df):
        
        return SBITransactionParser( txn_df)
    
    def set_start_index_string(self):

        return r"^\d{2}/\d{2}/\d{4}"
    


    

