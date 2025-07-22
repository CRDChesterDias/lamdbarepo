import openpyxl

def normalize(text):
    return str(text).strip().lower() if text else ""

def process_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    
    for sheet_name in wb.sheetnames:
        if not sheet_name.startswith("AAA_TO_BBB"):
            continue

        ws = wb[sheet_name]
        headers = [cell.value for cell in ws[1]]

        # Get column indexes
        col_index = {header: idx for idx, header in enumerate(headers)}

        required_cols = ["Source", "short desc", "Comments"]
        if not all(col in col_index for col in required_cols):
            print(f"Missing required columns in {sheet_name}")
            continue

        match_status_col = len(headers)
        if "Match_Status" not in headers:
            ws.cell(row=1, column=match_status_col + 1).value = "Match_Status"

        # Separate rows by Source
        aaa_rows = []
        bbb_rows = []

        for row_idx in range(2, ws.max_row + 1):
            row = [ws.cell(row=row_idx, column=i+1).value for i in range(len(headers))]
            if normalize(row[col_index["Source"]]) == "aaa":
                aaa_rows.append((row_idx, row))
            elif normalize(row[col_index["Source"]]) == "bbb":
                bbb_rows.append((row_idx, row))

        # Match BBB short desc with AAA
        for bbb_idx, bbb_row in bbb_rows:
            bbb_short = normalize(bbb_row[col_index["short desc"]])
            matched = False

            for _, aaa_row in aaa_rows:
                aaa_short = normalize(aaa_row[col_index["short desc"]])
                if bbb_short == aaa_short:
                    # Copy Comments from AAA to BBB
                    ws.cell(row=bbb_idx, column=col_index["Comments"]+1).value = aaa_row[col_index["Comments"]]
                    matched = True
                    break

            # Write match status
            status = "Matched" if matched else "Not Matched"
            ws.cell(row=bbb_idx, column=match_status_col + 1).value = status

    wb.save(file_path)
    print(f"✅ Completed processing and saved: {file_path}")
