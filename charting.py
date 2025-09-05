import pandas as pd
import matplotlib.pyplot as plt

# Path to your Excel file
excel_file = "vm_startup_report.xlsx"

# Read all sheets
all_sheets = pd.read_excel(excel_file, sheet_name=None)

# Number of sheets
num_sheets = len(all_sheets)

# Create subplots (adjust grid dynamically based on sheet count)
cols = 2
rows = (num_sheets + 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows))

# Flatten axes for easy iteration
axes = axes.flatten()

# Choose a bright color palette
color_palettes = plt.cm.Set3.colors  # bright pastel colors
# Alternatively: plt.cm.tab10.colors for 10 distinct bright colors

for i, (sheet_name, df) in enumerate(all_sheets.items()):
    if "Startup Status" not in df.columns:
        continue  # skip if sheet doesn't have expected column

    # Count values
    status_counts = df["Startup Status"].value_counts()

    # Plot pie chart in subplot
    axes[i].pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=color_palettes[:len(status_counts)],  # use bright colors
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    axes[i].set_title(f"{sheet_name} - Startup Status", fontsize=12)

# Hide any unused subplots (in case of uneven grid)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
