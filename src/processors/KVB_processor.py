from src.processors.base_processor import BaseProcessor
from src.parsers.KVB_transaction_parser import KVBParser
import sys
from src.exception import CustomException
from src.logger import logging


class KVBProcessor(BaseProcessor):

    def get_parser(self, filepath):
        
        return KVBParser(filepath)

    def transform(self):
        try:
            logging.info("Starting KVB Bank processing")

            # ---------------------------
            # Step 1: Ingestion and parsing
            # ---------------------------
           
            parser = self.get_parser(self.filepath)
            final_df = parser.transform()

            logging.info("KVB Bank processing completed")

            return final_df

        except Exception as e:
            logging.error("Error in KVB Bank processing")
            raise CustomException(e, sys)
        

# if __name__ == "__main__":
#     try:
#         processor = KVBProcessor('data/KVB.pdf')
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)