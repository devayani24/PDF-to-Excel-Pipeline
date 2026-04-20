from dataclasses import dataclass
from src.parsers.base_text_parser import BaseTextParser, BaseTextParserConfig


@dataclass
class IndianBankParserConfig(BaseTextParserConfig):
    date_patterns:  str   = r'(\d{2}\s\w{3}\s\d{4})'
    amount_pattern: str   = r'(?:(-)\sINR\s(.+)\sINR\s(.+))|(?:INR\s(.+)\s(-)\sINR\s(.+))'
    stop_markers:   tuple = ("Ending Balance", "Statement Summary")


class IndianBankParser(BaseTextParser):

    def _get_config(self) -> IndianBankParserConfig:
        return IndianBankParserConfig()