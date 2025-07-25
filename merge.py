import pandas as pd
import glob

# Path to your Excel files
folder_path = './your_folder_path/'  # Update this path
excel_files = glob.glob(folder_path + '*.xlsx')

# Create containers for each sheet type
ii_data_list = []
em_data_list = []

for file in excel_files:
    try:
        xls = pd.ExcelFile(file)
        if "II DATA" in xls.sheet_names:
            df_ii = xls.parse("II DATA")
            df_ii['SourceFile'] = file  # Optional: track origin
            ii_data_list.append(df_ii)

        if "EM DATA" in xls.sheet_names:
            df_em = xls.parse("EM DATA")
            df_em['SourceFile'] = file  # Optional
            em_data_list.append(df_em)

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Merge all data
merged_ii = pd.concat(ii_data_list, ignore_index=True)
merged_em = pd.concat(em_data_list, ignore_index=True)

# Save to new Excel with two sheets
with pd.ExcelWriter('merged_II_and_EM.xlsx') as writer:
    merged_ii.to_exc
