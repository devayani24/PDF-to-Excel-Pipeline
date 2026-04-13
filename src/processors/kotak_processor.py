from src.processors.base_processor import BaseProcessor
from src.parsers.kotak_transaction_parser import KotakTransactionParser,KotakConfig

import sys
from src.exception import CustomException

class KotakProcessor(BaseProcessor):

    def get_parser(self, txn_df):
        config = KotakConfig()
        return KotakTransactionParser(config, txn_df)
    
    def set_start_index_string(self):

        return r"^\d\s\d{2}\s\w{3}\s\d{4}"
    

# if __name__ == "__main__":
#     try:
#         filepath = 'data/kotak.pdf'
#         processor = KotakProcessor(filepath)
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)
    

