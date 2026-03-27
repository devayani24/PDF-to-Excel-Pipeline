import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List

# ---------------------------
# Export Function
# ---------------------------

def export_dataframe_to_csv(df: pd.DataFrame,file_name: str,dir_path: str = "artifacts")-> str:
    try:
        path: str = os.path.join(dir_path,file_name)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path),exist_ok=True)
    
        df.to_csv(path,index=False,header=True)
        logging.info(f"Exported DataFrame to CSV: {path}")

        return path

    except Exception as e:
        logging.error(f"Error while exporting DataFrame to csv {file_name}: {e}")
        raise CustomException(e, sys)

# ---------------------------
# Validation
# ---------------------------   

def dataframe_validation(*args: List):
    try: 
        if not args:
            raise ValueError("No data provided")
        
        lengths = [len(l) for l in args]
        
        if len(set(lengths))!=1:
            raise ValueError(f"List lengths mismatch: {lengths}")
        
        logging.info(f"Validation passed. Length: {lengths[0]}")

    except Exception as e:
        logging.error(f"Data validation failed: {e}")
        raise CustomException(e,sys)

# ---------------------------
# Convert Function
# ---------------------------
   
def convert_list_to_dataframe (*args: List,columns: List[str]) -> pd.DataFrame:
    try:
        if len(args) != len(columns):
            raise ValueError(
                f"Columns ({len(columns)}) and data lists ({len(args)}) mismatch"
            )

        dataframe_validation(*args)

        df = pd.DataFrame(dict(zip(columns, args)))

        logging.info(f"Created DataFrame with columns: {columns}")

        return df

    except Exception as e:
        logging.error("Error while converting lists to DataFrame")
        raise CustomException(e, sys)