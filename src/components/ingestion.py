import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import pdfplumber
from tabula.io import read_pdf
from typing import List,Tuple

from src.utils import export_dataframe_to_csv,convert_list_to_dataframe


class PDFPlumberReader():
    
    
    def extract_text_from_pdf(self, filepath: str, password: str) -> List[str]:
        """
        Extracts text line by line from a PDF file.
        """
        rows = []

        try:
            with pdfplumber.open(filepath, password=password) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()

                    if not text:
                        logging.warning(f"No text found on page {page_num}")
                        continue

                    # rows.extend(text.split("\n"))
                    for line in text.split("\n"):
                        rows.append(line)

            logging.info("PDF extraction completed successfully")
            return rows
        
        except Exception as e:
            logging.error(f"Error while extracting PDF: {filepath}")
            raise CustomException(e, sys)
        
    def to_dataframe(self, filepath: str, password: str = None) -> pd.DataFrame:
        try:
            rows = self.extract_text_from_pdf(filepath,  password = password)
        
            raw_df = convert_list_to_dataframe(rows, columns=["raw"])

            return raw_df

        except Exception as e:
            raise CustomException(e, sys)
        
    
        

class TabulaPDFReader():
    
    def read_tables(self, filepath: str) -> pd.DataFrame:
        try:
            tables = read_pdf(filepath, pages="all", multiple_tables=True)
            logging.info(f"Tabula extracted {len(tables)} tables from PDF")

            # Combine all pages
            final_df  = pd.concat(tables, ignore_index=True) 


            return final_df 
        
        except Exception as e:
            logging.error("Error in combine_full_transaction process")
            raise CustomException(e, sys)
        

class OCRReader():
    pass