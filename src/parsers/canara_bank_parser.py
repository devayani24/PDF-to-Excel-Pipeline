import re
from src.parsers.base_coordinate_parser import BaseCoordinateParser, ParserConfig

canara_column_list = ['Particulars','Deposits','Withdrawals','Balance']

class CanaraBankParser(BaseCoordinateParser):

    def _get_config(self):
        return ParserConfig(
            date_pattern            = r'\d{2}-\d{2}-\d{4}',
            default_top_1           = 435.984,   # fallback only
            default_top_other       = 64.484,    # fallback only
            crop_increment_1        = 40,
            crop_increment_other    = 24,
            x_date_max              = 30,
            x_particulars_min       = 30,
            x_particulars_max       = 300,
            x_withdrawal_min        = 400,
            x_withdrawal_max        = 500,
            x_deposit_min           = 300,
            x_deposit_max           = 400,
            x_balance_min           = 500,
            stop_markers            = ["Closing"],
            break_markers           = [],
            column_list             = ['Particulars','Deposits','Withdrawals','Balance']
            
        )

    def _fix_particulars(self, particulars):
        corrected = []
        buffer    = []
        found     = False

        for item in particulars:
            for w in item.split(' '):
                if found:
                    buffer.append(w)
                    corrected.append(" ".join(buffer))
                    buffer = []
                    found  = False
                    continue        # ← skip to next word, don't fall through

                if 'Chq:' in w:
                    buffer.append(w)
                    found = True
                else:
                    buffer.append(w)

        return corrected