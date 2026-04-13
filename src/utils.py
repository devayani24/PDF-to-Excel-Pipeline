import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List

# ---------------------------
# Export Function
# ---------------------------

def export_dataframe_to_csv(df: pd.DataFrame,file_name: str,output_folder: str)-> str:
    try:
        # ---------------------------
        # If user selected folder → use it
        # else fallback (optional)
        # ---------------------------
        if output_folder:
            full_dir_path = output_folder
        else:

            # ---------------------------
            # Base path (important for .exe)
            # ---------------------------
            if getattr(sys, 'frozen', False):
                full_dir_path = os.path.dirname(sys.executable)
            else:
                full_dir_path = os.getcwd()

        # Create directory if not exists
        os.makedirs(full_dir_path, exist_ok=True)

        # ---------------------------
        # Full file path
        # ---------------------------
        path = os.path.join(full_dir_path, file_name)


       
        # Save file
        df.to_csv(path, index=False, header=True)

        logging.info(f"Exported DataFrame to CSV: {path}")

        return path

    except Exception as e:
        logging.error(f"Error while exporting DataFrame to csv {file_name}: {e}")
        raise CustomException(e, sys)

# ---------------------------
# Validation
# ---------------------------   

def dataframe_validation(*args: List, columns: List[str] = None):
    try: 
        if not args:
            raise ValueError("No data provided")
        
        lengths = [len(l) for l in args]

        if len(set(lengths))!=1:
            # Debug export
            debug_lists_to_csv(**dict(zip(columns, args)))
            
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

        dataframe_validation(*args,columns=columns)

        df = pd.DataFrame(dict(zip(columns, args)))

        logging.info(f"Created DataFrame with columns: {columns}")

        return df

    except Exception as e:
        logging.error("Error while converting lists to DataFrame")
        raise CustomException(e, sys)
    

def debug_lists_to_csv(**kwargs):
    
    
    df = pd.DataFrame({
        key: pd.Series(value) for key, value in kwargs.items()
    })
    
    df.to_csv("debug_output.csv", index=False)