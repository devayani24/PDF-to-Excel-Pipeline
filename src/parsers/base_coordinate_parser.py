import sys
import re
import pdfplumber
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from src.exception import CustomException
from src.logger import logging
from src.utils import convert_list_to_dataframe


@dataclass
class ParserConfig:
    date_pattern:           str
    default_top_1:          float
    default_top_other:      float
    crop_increment_1:       int
    crop_increment_other:   int
    x_date_max:             float
    x_particulars_min:      float
    x_particulars_max:      float
    x_withdrawal_min:       float
    x_withdrawal_max:       float
    x_deposit_min:          float
    x_deposit_max:          float
    x_balance_min:          float
    stop_markers:           List[str] = field(default_factory=list)
    break_markers:          List[str] = field(default_factory=list)
    column_list:            List[str] = field(default_factory=list)


class BaseCoordinateParser:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = self._get_config()

    # ---------------------------
    # Must be implemented by each bank
    # ---------------------------
    def _get_config(self) -> ParserConfig:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _get_config()"
        )
    
    def get_bbox_text_top(self, page , column_list: list) -> float:

        if not column_list:
            return None
            
        words = page.extract_words()
        tops= []

        for w in words:
            text = w['text']
            if text in column_list:
                tops.append(w['top'])
            if text == column_list[-1]:
                break

        if tops and len(set(tops)) == 1:
            return tops[-1]

        return None

    # ---------------------------
    # Helper Methods
    # ---------------------------
    def _get_bbox(self, page, page_index: int, ) -> Tuple:
        
        increment   = self.config.crop_increment_1 if page_index == 0 else self.config.crop_increment_other
        default_top = self.config.default_top_1    if page_index == 0 else self.config.default_top_other

        top = self.get_bbox_text_top(page, self.config.column_list)

        if top is None:
            top = default_top
        else:
            top = top + increment

        return (0, top, page.width, page.height)

    def _should_stop(self, text: str) -> bool:
        return any(marker in text for marker in self.config.stop_markers)

    def _should_break(self, text: str) -> bool:
        return any(marker in text for marker in self.config.break_markers)

    def _fix_particulars(self, particulars: List[str]) -> List[str]:
        """Default — return as is. Override in subclass if needed."""
        return particulars

    # ---------------------------
    # Main Transform
    # ---------------------------
    def transform(self):
        try:
            cfg = self.config
            amt_pattern = r'.+\.\d{2}'

            dates, particulars, deposits, withdrawals, balances = [], [], [], [], []
            buffer = []
            prev_date = None
            stop_all = False

            with pdfplumber.open(self.filepath) as pdf:
                for i, page in enumerate(pdf.pages):

                    if stop_all:
                        break

                    bbox = self._get_bbox(page, i)
                    words = page.crop(bbox).extract_words()

                    if not words:
                        break

                    for w in words:
                        x    = w['x0']
                        text = w['text']

                        if self._should_stop(text):
                            stop_all = True
                            break

                        if self._should_break(text):
                            break

                        # New date detected
                        if x < cfg.x_date_max and re.search(cfg.date_pattern, text):
                            if prev_date is not None:
                                if buffer:
                                    particulars.append(" ".join(buffer))
                                    buffer = []
                                max_len = max(len(deposits), len(withdrawals), len(balances))
                                deposits    += [None] * (max_len - len(deposits))
                                withdrawals += [None] * (max_len - len(withdrawals))

                            prev_date = text
                            dates.append(text)

                        elif cfg.x_particulars_min < x < cfg.x_particulars_max:
                            buffer.append(text)

                        elif cfg.x_withdrawal_min < x < cfg.x_withdrawal_max and re.search(amt_pattern, text):
                            withdrawals.append(text)

                        elif cfg.x_deposit_min < x < cfg.x_deposit_max and re.search(amt_pattern, text):
                            deposits.append(text)

                        elif x > cfg.x_balance_min and re.search(amt_pattern, text):
                            balances.append(text)

            # Final balancing
            max_len = max(len(deposits), len(withdrawals), len(balances))
            deposits    += [None] * (max_len - len(deposits))
            withdrawals += [None] * (max_len - len(withdrawals))

            if buffer:
                particulars.append(" ".join(buffer))


            corrected_particulars = self._fix_particulars(particulars)

            return convert_list_to_dataframe(
                dates, corrected_particulars, withdrawals, deposits, balances,
                columns=['Date', 'Transactional details', 'Debit', 'Credit', 'Balance']
            )

        except Exception as e:
            logging.error("Error in transform process")
            raise CustomException(e, sys)