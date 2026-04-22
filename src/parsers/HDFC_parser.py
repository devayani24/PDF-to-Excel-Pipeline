from src.parsers.base_coordinate_parser import BaseCoordinateParser, ParserConfig

class HDFCTransactionParser(BaseCoordinateParser):

    def _get_config(self):
        return ParserConfig(
            date_pattern            = r'\d{2}/\d{2}/\d{2}',
            default_top_1           = 233,   # fallback only
            default_top_other       = 230,    # fallback only
            crop_increment_1        = 30,
            crop_increment_other    = 20,
            x_date_max              = 50,
            x_particulars_min       = 50,
            x_particulars_max       = 100,
            x_withdrawal_min        = 430,
            x_withdrawal_max        = 510,
            x_deposit_min           = 510,
            x_deposit_max           = 580,
            x_balance_min           = 520,
            stop_markers            = ["STATEMENTSUMMARY"],
            break_markers           = ["HDFCBANKLIMITED"],
            column_list             = ['Statementof']
        )