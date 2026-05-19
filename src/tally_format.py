import pandas as pd

def convert_to_tally_format(df, bank_ledger="Indian Bank"):

    # Step 1 — Clean amounts and Date format
    def clean_amount(val):
        if pd.isna(val):
            return ""
        val = str(val).strip()
        return "" if val in ['-', '', 'None', 'nan'] else val

    df['Debit']  = df['Debit'].apply(clean_amount)
    df['Credit'] = df['Credit'].apply(clean_amount)

    def convert_Date(val):
        try:
            return pd.to_Datetime(val, dayfirst=True).strftime('%d-%m-%Y')
        except:
            return val  # return as is if conversion fails

    df['Date'] = df['Date'].apply(convert_Date)

    # Step 2 — Voucher type
    df['VoucherTypeName'] = df.apply(
        lambda x: 'Receipt' if x['Credit'] != "" else 'Payment', axis=1
    )

    # Step 3 — Separate voucher numbers per type
    df['VoucherNumber'] = df.groupby('VoucherTypeName').cumcount() + 1

    # Step 4 — Amount
    df['LedgerAmount'] = df.apply(
        lambda x: x['Credit'] if x['Credit'] != "" else x['Debit'], axis=1
    )

    # Step 5 — Build two rows per transaction
    rows = []

    for _, row in df.iterrows():
        Date      = row['Date']
        narration = row['Transaction_details']
        vtype     = row['VoucherTypeName']
        vnum      = row['VoucherNumber']
        amount    = row['LedgerAmount']

        # Named ledger — always Sus for payments, Online Receipts for receipts
        named_ledger = 'Online Receipts' if vtype == 'Receipt' else 'Sus'

        # Dr/Cr for bank ledger
        bank_dr_cr  = 'Dr' if vtype == 'Receipt' else 'Cr'

        # Dr/Cr for named ledger
        named_dr_cr = 'Cr' if vtype == 'Receipt' else 'Dr'

        common = {
            'Voucher Date'              : Date,
            'Voucher Type Name'          : vtype,
            'Voucher Number'            : vnum,
            'Ledger Amount'             : amount,
            'Voucher Narration'         : narration,
            'Buyer/Supplier - Address' : None,
            'Buyer/Supplier - Pincode' : None,
            'Item Name'                : None,
            'Billed Quantity'          : None,
            'Item Rate'                : None,
            'Item Rate per'            : None,
            'Item Amount'              : None,
            'Change Mode'              : None,
        }

        # Row 1 — Bank ledger
        rows.append({**common,
            'Ledger Name'        : bank_ledger,
            'Ledger Amount Dr/Cr' : bank_dr_cr
        })

        # Row 2 — Named ledger (Sus or Online Receipts)
        rows.append({**common,
            'Ledger Name'        : named_ledger,
            'Ledger Amount Dr/Cr' : named_dr_cr
        })

    # Step 6 — Final DataFrame
    result = pd.DataFrame(rows)[[
        "Voucher Date",
        "Voucher Type Name",
        "Voucher Number",
        "Buyer/Supplier - Address",
        "Buyer/Supplier - Pincode",
        "Ledger Name",
        "Ledger Amount",
        "Ledger Amount Dr/Cr",
        "Item Name",
        "Billed Quantity",
        "Item Rate",
        "Item Rate per",
        "Item Amount",
        "Change Mode",
        "Voucher Narration"
    ]]

    return result.sort_values(
        by=["Voucher Number", "Voucher Type Name"]
    ).reset_index(drop=True)


