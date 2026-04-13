import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from tabula.io import read_pdf
from src.processors.base_processor import BaseProcessor
from src.components.ingestion import TabulaPDFReader

class CityUnionBankProcessor(BaseProcessor):


    # def get_parser(self, txn_df: pd.DataFrame):
    #     """
    #     This will be overridden in child classes
    #     """
    #     return BaseTransactionParser(txn_df)

    def transform(self) -> pd.DataFrame:
        try:
            logging.info("Starting City Union Bank processing")

            # ---------------------------
            # Step 1: Ingestion abd Transformation
            # ---------------------------
            reader = TabulaPDFReader()
            final_df = reader.read_tables(self.filepath)

            

            logging.info("City Union Bank processing completed")

            return final_df

        except Exception as e:
            logging.error("Error in City Union Bank processing")
            raise CustomException(e, sys)

# if __name__ == "__main__":
#     try:
#         processor = CityUnionBankProcessor('data/City_1.pdf')
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)
    