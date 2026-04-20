from src.processors.base_coordinate_processor import BaseCoordinateProcessor
from src.parsers.HDFC_parser import HDFCTransactionParser


class HDFCProcessor(BaseCoordinateProcessor):
    def get_parser(self, filepath):
        return HDFCTransactionParser(filepath)