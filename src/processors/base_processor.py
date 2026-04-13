import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from src.components.ingestion import PDFPlumberReader
from src.components.transformation import DataTransformer
from src.parsers.base_transaction_parser import BaseTransactionParser


class BaseProcessor:

    def __init__(self, filepath: str, password: str = None):
        self.filepath = filepath
        self.password = password
        

    def get_parser(self, txn_df: pd.DataFrame):
        """
        This will be overridden in child classes
        """
        return BaseTransactionParser(txn_df)
    
    
    def set_start_index_string(self):

        return r"^\d{2}\s\w{3}\s\d{4}"

    def transform(self) -> pd.DataFrame:
        try:
            logging.info("Starting Indian Bank processing")

            # ---------------------------
            # Step 1: Ingestion
            # ---------------------------
            reader = PDFPlumberReader()
            raw_df = reader.to_dataframe(self.filepath, self.password)

            # ---------------------------
            # Step 2: Transformation
            # ---------------------------
            transformer = DataTransformer(raw_df, start_index_string = self.set_start_index_string())
            txn_df  = transformer.transform()

            # ---------------------------
            # Step 3: Parsing
            # ---------------------------
            parser = self.get_parser(txn_df)
            final_df = parser.transform()

            logging.info("Indian Bank processing completed")

            return final_df

        except Exception as e:
            logging.error("Error in Indian Bank processing")
            raise CustomException(e, sys)
        
        





        
        






