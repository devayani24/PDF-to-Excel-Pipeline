from src.processors.base_coordinate_processor import BaseCoordinateProcessor
from src.parsers.city_union_parser import CityUnionTransactionParser

class CityUnionProcessor(BaseCoordinateProcessor):
    def get_parser(self, filepath):
        return CityUnionTransactionParser(filepath)