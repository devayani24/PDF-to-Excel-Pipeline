import sys
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from typing import List,Tuple
from src.utils import export_dataframe_to_csv,convert_list_to_dataframe
import pdfplumber

class CanaraBankParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def transform(self):
        dates = []
        particulars = []
        deposits = []
        withdrawals = []
        balances = []

        amt_pattern = r'.+\.\d{2}'
        date_pattern = r'\d{2}-\d{2}-\d{4}'

        prev_date = None
        stop_all = False

        with pdfplumber.open(self.filepath) as pdf:
            for i in range(len(pdf.pages)):
                if stop_all:
                    break

                page = pdf.pages[i]

                if i == 0:
                    bbox = (0, 435.984, page.width, page.height)
                else:
                    bbox = (0, 64.48400000000004, page.width, page.height)

                words = page.crop(bbox).extract_words()

                for w in words:
                    x = w['x0']
                    text = w['text']

                    if 'Closing' in text:
                        stop_all = True
                        break

                    if (x < 30) and re.search(date_pattern, text):

                        if prev_date is not None:
                            max_len = max(len(deposits), len(withdrawals), len(balances))

                            deposits += [None] * (max_len - len(deposits))
                            withdrawals += [None] * (max_len - len(withdrawals))
                            

                        prev_date = text
                        dates.append(text)

                    elif (30 < x < 300):
                        particulars.append(text)

                    elif (300 < x < 400) and re.search(amt_pattern, text):
                        deposits.append(text)

                    elif (400 < x < 500) and re.search(amt_pattern, text):
                        withdrawals.append(text)

                    elif (x > 500) and re.search(amt_pattern, text):
                        balances.append(text)

        # Final balancing
        max_len = max(len(deposits), len(withdrawals), len(balances))

        deposits += [None] * (max_len - len(deposits))
        withdrawals += [None] * (max_len - len(withdrawals))
       

        # Fix particulars
        corrected_particulars = []
        current = []
        found = False

        for item in particulars:
            if found:
                current.append(item)
                corrected_particulars.append(" ".join(current))
                current = []
                found = False
            else:
                current.append(item)

            if re.match(r'^Chq:$', item):
                found = True

        if current:
            corrected_particulars.append(" ".join(current))

        # DataFrame
        df = convert_list_to_dataframe (dates,corrected_particulars,withdrawals,deposits,balances, columns=['Date', 'Transactional details', 'Debit','Credit','Balance'])
        
        return df