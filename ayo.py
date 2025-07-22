import openpyxl

def normalize_short_desc(text):
    return str(text).strip().lower()[:111] if text else ""

def process_excel(file_path):
    wb = openpyxl.load_workbook(file_path)

    for sheet_name in wb.sheetnames:
        if not sheet_name.startswith("AAA_TO_BBB"):
            continue

        ws = wb[sheet_name]
        headers = [cell.value for cell in ws[1]]
        col_index = {header: idx for idx, header in enumerate(headers)}

        if "Source" not in col_index or "short desc" not in col_index or "Comments" not in col_index:
            print(f"⚠️ Required columns missing in sheet {sheet_name}")
            continue

        aaa_rows = []
        bbb_rows = []

        # Collect AAA and BBB rows with original formatting
        for row_idx in range(2, ws.max_row + 1):
            row_data = [ws.cell(row=row_idx, column=col+1).value for col in range(len(headers))]
            source = str(row_data[col_index["Source"]]).strip().lower()
            if source == "aaa":
                aaa_rows.append((row_idx, row_data))
            elif source == "bbb":
                bbb_rows.append((row_idx, row_data))

        # Build a lookup dictionary for AAA by short desc (first 111 chars, lowercase)
        aaa_lookup = {
            normalize_short_desc(r[col_index["short desc"]]): r
            for _, r in aaa_rows
        }

        # Extend headers with AAA columns (with _AAA suffix) if not already present
        extended_cols = [h + "_AAA" for h in headers]
        for new_col in extended_cols:
            if new_col not in col_index:
                ws.cell(row=1, column=len(col_index) + 1).value = new_col
                col_index[new_col] = len(col_index)

        for row_idx, bbb_row in bbb_rows:
            key = normalize_short_desc(bbb_row[col_index["short desc"]])
            matched_row = aaa_lookup.get(key)

            if matched_row:
                # Match found — add data from AAA row into BBB row under new columns
                for i, value in enumerate(matched_row):
                    ws.cell(row=row_idx, column=col_index[headers[i] + "_AAA"] + 1).value = value

                # Write "Matched" into Comments
                ws.cell(row=row_idx, column=col_index["Comments"] + 1).value = "Matched"
            else:
                # No match — retain BBB's original Comments
                ws.cell(row=row_idx, column=col_index["Comments"] + 1).value = bbb_row[col_index["Comments"]]

    wb.save(file_path)
    print(f"✅ Finished processing and saved: {file_path}")
