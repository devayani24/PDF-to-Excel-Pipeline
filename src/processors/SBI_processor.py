from src.processors.base_processor import BaseProcessor
from src.parsers.SBI_transaction_parser import SBITransactionParser

import sys
from src.exception import CustomException

class SBIProcessor(BaseProcessor):

    def get_parser(self, txn_df):
        
        return SBITransactionParser( txn_df)
    
    def set_start_index_string(self):

        return r"^\d{2}/\d{2}/\d{4}"
    

# if __name__ == "__main__":
#     try:
        
#         filepath = 'data/SBI.pdf'
#         password = 'SELVA26021996'
#         processor = SBIProcessor(filepath, password = password)
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)
    

