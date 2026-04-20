from src.parsers.base_coordinate_parser import BaseCoordinateParser, ParserConfig

class KVBParser(BaseCoordinateParser):

    def _get_config(self):
        return ParserConfig(
            date_pattern        = r'\d{2}/\d{2}/\d{4}',
            bbox_first_page     = (0, 348.074, None, None),
            bbox_other_pages    = (0, 348.074, None, None),
            x_date_max          = 50,
            x_particulars_min   = 160,
            x_particulars_max   = 390,
            x_withdrawal_min    = 390,
            x_withdrawal_max    = 450,
            x_deposit_min       = 450,
            x_deposit_max       = 510,
            x_balance_min       = 510,
            stop_markers        = [],
            break_markers       = [],
        )