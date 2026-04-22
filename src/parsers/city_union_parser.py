from src.parsers.base_coordinate_parser import BaseCoordinateParser, ParserConfig

class CityUnionTransactionParser(BaseCoordinateParser):

    def _get_config(self):
        return ParserConfig(
            date_pattern            = r'\d{2}/\d{2}/\d{4}',
            default_top_1           = 594,
            default_top_other       = 171,
            crop_increment_1        = 20,
            crop_increment_other    = 20,
            x_date_max              = 30,
            x_particulars_min       = 118,
            x_particulars_max       = 770,
            x_withdrawal_min        = 770,
            x_withdrawal_max        = 900,
            x_deposit_min           = 900,
            x_deposit_max           = 1000,
            x_balance_min           = 1000,
            stop_markers            = ["TOTAL"],
            break_markers           = ["Regd."],
            column_list             = ['DESCRIPTION', 'CHEQUE', 'DEBIT', 'CREDIT']
        )