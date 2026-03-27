
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import pdfplumber

from src.components.transformation import DataTransformation
from src.components.transaction_parser import TransactionParser
from src.utils import export_dataframe_to_csv,convert_list_to_dataframe
from typing import List,Tuple


    

class DataIngestion:

    # ---------------------------
    # UI
    # ---------------------------

    @staticmethod
    def display():

        print('\n')
        print('Enter the bank number from the below list')
        print('*'*100)
        print('1: Indian bank\n2: SBI\n3: HDFC\n4: Canara bank')
        print('*'*100)

    def get_choice_filepath_from_user(self)-> Tuple[int, str]:

        
        try:
            choice = int(input("Please enter here: "))
            if choice not in [1, 2, 3, 4]:
                raise ValueError("Choice must be between 1 and 4")
            print('\n')
            filepath = input("Enter the pdf file location: ")

            

            return choice, filepath

            
        except Exception as e:
            logging.info("Invalid inputfrom user")
            raise CustomException(e,sys)
    
    # ---------------------------
    # Core Logic
    # ---------------------------
    
    def extract_text_from_pdf(self, filepath: str) -> List[str]:
        """
        Extracts text line by line from a PDF file.
        """
        rows = []

        try:
            with pdfplumber.open(filepath) as pdf:
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

        
    def process_based_on_choice(self, choice: int, filepath: str) -> List[str]:

        rows = self.extract_text_from_pdf(filepath)
        if choice == 1:
                logging.info("Processing Indian Bank PDF")
                return rows

        elif choice == 2:
            logging.info("SBI logic not implemented yet")

        elif choice == 3:
            logging.info("HDFC logic not implemented yet")

        elif choice == 4:
            logging.info("Canara Bank logic not implemented yet")

        return rows  
      
    # ---------------------------
    # Main Pipeline Step
    # ---------------------------
      
    def get_dataframe(self) -> pd.DataFrame:
        try:
            logging.info("Starting data ingestion")

            self.display()
            choice, filepath = self.get_choice_filepath_from_user()

            rows = self.process_based_on_choice(choice, filepath)

            raw_df = convert_list_to_dataframe(rows, columns=["raw"])

            export_dataframe_to_csv(raw_df, "raw.csv")

            logging.info("Data ingestion completed successfully")

            return raw_df

        except Exception as e:
            raise CustomException(e, sys)
        
    # ---------------------------
    # Entry Point (Best Practice)
    # ---------------------------
    def run(self) -> pd.DataFrame:
        return self.get_dataframe()
    

if __name__ == "__main__":
    try:
        ingestion = DataIngestion()
        raw_dataframe = ingestion.run()

        # Transformation
        data_trans = DataTransformation(raw_dataframe)
        txn_df = data_trans.initial_data_transformation()

        # Transaction Split
        splitter = TransactionParser(txn_df)
        final_df = splitter.transform()

        export_dataframe_to_csv(final_df, "AccountStatement.csv")

        print(final_df.head())

    except Exception as e:
        raise CustomException(e, sys)