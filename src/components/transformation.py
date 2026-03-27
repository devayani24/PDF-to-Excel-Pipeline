import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging


class DataTransformation:
    def __init__ (self,df:pd.DataFrame,raw_column: str = "raw"):
        self.df=df
        self.raw_column = raw_column
        
    # ---------------------------
    # Helper Methods
    # ---------------------------

    def get_first_transaction_index(self) -> int:
        try:
            logging.info("Finding first transaction index")

            mask = self.df[self.raw_column].str.contains(
                "Date", case=False, na=False
            )

            indices = self.df.loc[mask].index

            if len(indices) == 0:
                raise ValueError("No 'Date' keyword found in data")

            return int(indices[0]) + 1
        
        except Exception as e:
            logging.error("Error while finding first transaction index")
            raise CustomException(e, sys)
        
    # ---------------------------
    # Main Transformation
    # ---------------------------

    def initial_data_transformation(self) -> pd.DataFrame:
        try:
            logging.info("Starting initial data transformation")

            start_idx = self.get_first_transaction_index()

            transaction_df = self.df.loc[start_idx:].reset_index(drop=True)

            logging.info("Initial data transformation completed")

            return transaction_df

        except Exception as e:
            logging.error("Error in initial data transformation")
            raise CustomException(e, sys)
    


