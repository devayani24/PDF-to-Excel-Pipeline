from src.processors.base_coordinate_processor import BaseCoordinateProcessor
from src.parsers.KVB_parser import KVBParser


class KVBProcessor(BaseCoordinateProcessor):
    def get_parser(self, filepath):
        return KVBParser(filepath)