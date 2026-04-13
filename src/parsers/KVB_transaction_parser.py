import sys
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List,Tuple
from src.utils import export_dataframe_to_csv,convert_list_to_dataframe
from src.parsers.canara_bank_parser import CanaraBankParser
import pdfplumber

class KVBParser(CanaraBankParser) :
    

    def transform(self):
        dates = []
        particulars = []
        deposits = []
        withdrawals = []
        balances = []

        buffer = []

        amt_pattern = r'.+\.\d{2}'

        date_pattern = r'\d{2}/\d{2}/\d{4}'

        prev_date = None
        

        with pdfplumber.open(self.filepath) as pdf:
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                bbox = (0, 348.07401164074525, page.width, page.height )
                cropped_page = page.crop(bbox)
                words = cropped_page.extract_words()

                if not re.search(date_pattern, words[0]["text"]):
                    break

                for w in words:
                    x = w['x0']
                    text = w['text']

                    # 🔴 Detect new date
                    if (x < 50) and re.search(date_pattern, text):

                        if prev_date is not None:
                            
                            # finish previous row
                            if buffer:
                                particulars.append(" ".join(buffer))
                                buffer = []
                            
                            max_len = max(len(deposits), len(withdrawals), len(balances))
                            deposits += [None] * (max_len - len(deposits))
                            withdrawals += [None] * (max_len - len(withdrawals))
                            
                        prev_date = text
                        dates.append(text)

                    # 🔹 Continue filling row
                    elif (160 < x < 390):
                        buffer.append(text)
                        
                    elif (390 < x < 450)and re.search(amt_pattern, text):
                        withdrawals.append(text)

                    elif (450 < x < 510)and re.search(amt_pattern, text):
                        deposits.append(text)

                    elif (x > 510) and re.search(amt_pattern, text):
                        balances.append(text)
                    


        # 🔴 Final row fix
        max_len = max(len(deposits), len(withdrawals), len(balances))
        deposits += [None] * (max_len - len(deposits))
        withdrawals += [None] * (max_len - len(withdrawals))
       
        if buffer:
            particulars.append(" ".join(buffer))

        # DataFrame
        df = convert_list_to_dataframe (dates,particulars,withdrawals,deposits,balances, columns=['Date', 'Transactional details', 'Debit','Credit','Balance'])
        
        return df