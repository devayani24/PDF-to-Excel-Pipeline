import sys
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List,Tuple
from src.utils import convert_list_to_dataframe
import pdfplumber
from src.parsers.canara_bank_parser import CanaraBankParser

class HDFCTransactionParser(CanaraBankParser) :
    

    def transform(self):
        dates = []
        particulars = []
        deposits = []
        withdrawals = []
        balances = []

        buffer = []

        amt_pattern = r'.+\.\d{2}'

        date_pattern = r'\d{2}/\d{2}/\d{2}'

        prev_date = None

        stop_all = False

        with pdfplumber.open(self.filepath) as pdf:
            for i in range(len(pdf.pages)):

                if stop_all:
                    break
                page = pdf.pages[i]
                
                if i == 0:
                    bbox = (0, 233, page.width, page.height)
                else:
                    bbox = (0, 230, page.width, page.height)
            
                cropped_page = page.crop(bbox)
                words = cropped_page.extract_words()


                for w in words:
                    x = w['x0']
                    text = w['text']

                    if 'STATEMENTSUMMARY' in text:
                        stop_all = True
                        break
                    if 'HDFCBANKLIMITED' in text:
                        break

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
                    elif (50 < x < 100):
                        buffer.append(text)
                        
                    elif (430 < x < 510)and re.search(amt_pattern, text):
                        withdrawals.append(text)

                    elif (510 < x < 580)and re.search(amt_pattern, text):
                        deposits.append(text)

                    elif (x > 520) and re.search(amt_pattern, text):
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