import sys
from src.exception import CustomException
from src.processors.base_processor import BaseProcessor
from src.parsers.base_transaction_parser import BaseTransactionParser


class IndianBankProcessor(BaseProcessor):

    def get_parser(self, txn_df):
        return BaseTransactionParser(txn_df)
    


# if __name__ == "__main__":
#     try:
#         processor = IndianBankProcessor('data/IndianBank.pdf')
#         df = processor.transform()
#         output_path = processor.export(df)
#         print(output_path)

        

#     except Exception as e:
#         raise CustomException(e, sys)