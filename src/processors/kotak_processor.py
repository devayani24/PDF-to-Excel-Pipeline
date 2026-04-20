from src.processors.base_text_processor import BaseTextProcessor
from src.parsers.kotak_parser import KotakTransactionParser


class KotakProcessor(BaseTextProcessor):

    def get_parser(self, txn_df):
        return KotakTransactionParser(txn_df)

    def set_start_index_string(self):
        return r"^\d\s\d{2}\s\w{3}\s\d{4}"

# if __name__ == "__main__":
#     try:
#         filepath = 'data/kotak.pdf'
#         processor = KotakProcessor(filepath)
#         df = processor.transform()
#         df.to_csv(f"output.csv")

        

#     except Exception as e:
#         raise CustomException(e, sys)
    

