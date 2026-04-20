import sys
sys.path.insert(0, ".")

from src.processors.base_coordinate_processor import BaseCoordinateProcessor
from src.parsers.canara_bank_parser import CanaraBankParser

class CanaraBankProcessor(BaseCoordinateProcessor):
    def get_parser(self, filepath):
        return CanaraBankParser(filepath)
    

