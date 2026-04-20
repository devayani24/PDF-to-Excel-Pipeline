from src.processors.base_text_processor import BaseTextProcessor
from src.parsers.indian_bank_parser import IndianBankParser


class IndianBankProcessor(BaseTextProcessor):
    def get_parser(self, txn_df):
        return IndianBankParser(txn_df)
    
    def set_start_index_string(self):
        return r"^\d{2}\s\w{3}\s\d{4}"