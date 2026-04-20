import sys
from src.exception import CustomException
from src.logger import logging


class BaseCoordinateProcessor:

    def __init__(self, filepath: str, password: str = None):
        self.filepath = filepath
        self.password = password

    def get_parser(self, filepath: str):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_parser()"
        )

    def transform(self):
        try:
            logging.info(f"Starting {self.__class__.__name__} processing")

            parser = self.get_parser(self.filepath)
            final_df = parser.transform()

            logging.info(f"{self.__class__.__name__} processing completed")

            return final_df

        except Exception as e:
            logging.error(f"Error in {self.__class__.__name__} processing")
            raise CustomException(e, sys)