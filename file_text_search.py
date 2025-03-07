import pandas as pd

def find_rows_with_password(file_path, sheet_name=0):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)  # Read as string to avoid NaN issues

    # Convert to lowercase and check for 'password' in any column
    matching_rows = df[df.apply(lambda row: row.astype(str).str.contains('password', case=False, na=False).any(), axis=1)]

    return matching_rows

if __name__ == "__main__":
    excel_file = "your_excel_file.xlsx"  # Change this to your Excel file path
    result = find_rows_with_password(excel_file)

    if not result.empty:
        print("Rows containing the word 'password':")
        print(result)
    else:
        print("No rows found containing the word 'password'.")
