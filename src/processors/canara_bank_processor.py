from src.processors.base_processor import BaseProcessor
from src.parsers.canara_bank_parser import CanaraBankParser
import sys
from src.exception import CustomException
from src.logger import logging


class CanaraBankProcessor(BaseProcessor):

    def get_parser(self, filepath):
        
        return CanaraBankParser(filepath)

    def transform(self):
        try:
            logging.info("Starting Canara Bank processing")

            # ---------------------------
            # Step 1: Ingestion and parsing
            # ---------------------------
           
            parser = self.get_parser(self.filepath)
            final_df = parser.transform()

            logging.info("Canara Bank processing completed")

            return final_df

        except Exception as e:
            logging.error("Error in Canara Bank processing")
            raise CustomException(e, sys)
        

# if __name__ == "__main__":
#     try:
#         processor = CanaraBankProcessor('data/CanaraBank.pdf')
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)