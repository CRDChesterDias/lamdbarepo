import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# Config
filename = "your_excel_file.xlsx"
wb = load_workbook(filename)
columns_to_match = ['short desc']
sheet_pattern = "AAA_TO_BBB"

# Helper to normalize text
def normalize(text):
    return str(text).strip().lower() if pd.notnull(text) else ""

# Process each sheet
for sheet_name in wb.sheetnames:
    if not sheet_name.startswith(sheet_pattern):
        continue

    ws = wb[sheet_name]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    # Get column indexes
    col_idx = {h.lower(): i for i, h in enumerate(headers)}

    # Identify rows
    aaa_rows = []
    bbb_map = {}

    for row in ws.iter_rows(min_row=2, values_only=False):
        source = normalize(row[col_idx['source']].value)
        short_desc = normalize(row[col_idx['short desc']].value)
        comment_cell = row[col_idx['comments']]

        if source == 'bbb':
            bbb_map[short_desc] = comment_cell.value
        elif source == 'aaa':
            aaa_rows.append((short_desc, comment_cell))

    # Match and update comments
    for short_desc, cell in aaa_rows:
        if short_desc in bbb_map:
            cell.value = bbb_map[short_desc]
            # formatting (color etc.) is preserved automatically

# Save output
wb.save("updated_" + filename)
