import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging



class DataTransformer:
    def __init__ (self,df:pd.DataFrame, start_index_string: str, raw_column: str = "raw"):
        self.df=df
        self.raw_column = raw_column
        self.start_index_string = start_index_string

        
    # ---------------------------
    # Helper Methods
    # ---------------------------

    def find_transaction_start_index(self) -> int:
        try:
            logging.info("Finding first transaction index")

            mask = self.df[self.raw_column].str.contains(self.start_index_string, case=False, na=False)

            indices = self.df.loc[mask].index

            if len(indices) == 0:
                raise ValueError("No 'Date' keyword found in data")

            return int(indices[0])
        
        except Exception as e:
            logging.error("Error while finding first transaction index")
            raise CustomException(e, sys)
        
    # ---------------------------
    # Main Transformation
    # ---------------------------

    def transform(self) -> pd.DataFrame:
        try:
            logging.info("Starting initial data transformation")

            start_idx = self.find_transaction_start_index()

            if start_idx >= len(self.df):
                raise ValueError("Start index exceeds dataframe length")

            logging.info(f"First transaction starts at index: {start_idx}")

            transaction_df = self.df.loc[start_idx:].reset_index(drop=True)

            logging.info("Initial data transformation completed")

            return transaction_df

        except Exception as e:
            logging.error("Error in initial data transformation")
            raise CustomException(e, sys)
    


