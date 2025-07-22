import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

filename = "your_excel_file.xlsx"
wb = load_workbook(filename)
sheet_pattern = "AAA_TO_BBB"

def normalize(text):
    return str(text).strip().lower() if text else ""

for sheet_name in wb.sheetnames:
    if not sheet_name.startswith(sheet_pattern):
        continue

    ws = wb[sheet_name]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    col_idx = {str(h).strip().lower(): i for i, h in enumerate(headers)}

    # Create or get 'Match Status' column
    if 'match status' not in col_idx:
        match_col_letter = get_column_letter(len(headers) + 1)
        ws[f"{match_col_letter}1"] = "Match Status"
        match_col_idx = len(headers)
    else:
        match_col_idx = col_idx['match status']

    aaa_rows = []
    bbb_map = {}

    for row in ws.iter_rows(min_row=2):
        source = normalize(row[col_idx['source']].value)
        short_desc = normalize(row[col_idx['short desc']].value)
        comment_cell = row[col_idx['comments']]

        if source == 'bbb':
            bbb_map[short_desc] = comment_cell.value
        elif source == 'aaa':
            aaa_rows.append((row, short_desc, comment_cell))

    for row, short_desc, comment_cell in aaa_rows:
        match_value = bbb_map.get(short_desc)
        if match_value is not None:
            comment_cell.value = match_value
            row[match_col_idx].value = "Matched"
        else:
            row[match_col_idx].value = "Not Matched"

wb.save("updated_" + filename)
