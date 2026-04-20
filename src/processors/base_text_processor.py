# src/processors/base_text_processor.py
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.components.ingestion import PDFPlumberReader
from src.components.transformation import DataTransformer
from src.parsers.base_text_parser import BaseTextParser


class BaseTextProcessor:

    def __init__(self, filepath: str, password: str = None):
        self.filepath = filepath
        self.password = password

    def get_parser(self, txn_df: pd.DataFrame):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_parser()"
        )

    def set_start_index_string(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement set_start_index_string()"
        )

    def transform(self) -> pd.DataFrame:
        try:
            logging.info(f"Starting {self.__class__.__name__} processing")

            # Step 1: Ingestion
            reader = PDFPlumberReader()
            raw_df = reader.to_dataframe(self.filepath, self.password)

            # Step 2: Transformation
            transformer = DataTransformer(raw_df, start_index_string=self.set_start_index_string())
            txn_df = transformer.transform()

            # Step 3: Parsing
            parser = self.get_parser(txn_df)
            final_df = parser.transform()

            logging.info(f"{self.__class__.__name__} processing completed")

            return final_df

        except Exception as e:
            logging.error(f"Error in {self.__class__.__name__} processing")
            raise CustomException(e, sys)