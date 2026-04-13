from src.processors.base_processor import BaseProcessor
from src.parsers.HDFC_transaction_parser import HDFCTransactionParser

import sys
from src.exception import CustomException
from src.logger import logging

class HDFCProcessor(BaseProcessor):

    def get_parser(self, txn_df):
        
        return HDFCTransactionParser( txn_df)
    
    def transform(self):
        try:
            logging.info("Starting HDFC Bank processing")

            # ---------------------------
            # Step 1: Ingestion and parsing
            # ---------------------------
           
            parser = self.get_parser(self.filepath)
            final_df = parser.transform()

            logging.info("HDFC Bank processing completed")

            return final_df

        except Exception as e:
            logging.error("Error in HDFC Bank processing")
            raise CustomException(e, sys)
        

# if __name__ == "__main__":
#     try:
#         processor = HDFCProcessor('data/HDFC_1.pdf')
#         df = processor.transform()
#         df.to_csv(f"output.csv")

#     except Exception as e:
#         raise CustomException(e, sys)