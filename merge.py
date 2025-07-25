import pandas as pd
import glob

folder_path = './excels_folder/'

# Get all Excel files in the folder
excel_files = glob.glob(folder_path + '*.xlsx')

all_dfs = []

for file in excel_files:
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        all_dfs.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(all_dfs, ignore_index=True)

# Save merged data
merged_df.to_excel('merged_all_files.xlsx', index=False)

print("Merged data from all files shape:", merged_df.shape)
