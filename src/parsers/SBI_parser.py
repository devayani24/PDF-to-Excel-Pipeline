import re
from dataclasses import dataclass
from typing import Tuple
from src.parsers.base_text_parser import BaseTextParser, BaseTextParserConfig


@dataclass
class SBIParserConfig(BaseTextParserConfig):
    date_patterns:  str   = r'(\d{2}/\d{2}/\d{4})'
    amount_pattern: str   = ""
    stop_markers:   tuple = ("Statement Summary",)

class SBITransactionParser(BaseTextParser):

    def _get_config(self) -> SBIParserConfig:
        return SBIParserConfig()

    def extract_amounts(self, line: str) -> Tuple[str, str, str]:
        split_line = line.split(" ")
        return split_line[-3], split_line[-2], split_line[-1]

    def extract_transaction_details(self, line: str) -> str:
        temp = re.sub(self.config.date_patterns, "", line)
        return " ".join(temp.split(" ")[:-4]).strip()
    


    