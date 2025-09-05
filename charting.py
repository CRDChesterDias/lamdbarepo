import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Generate dummy data for 4 sheets, each with 50 entries
sheets_data = {}
statuses = ["Running", "Stopped", "Pending"]
num_entries = 50

for sheet_num in range(1, 5):
    df = pd.DataFrame({
        "Host": [f"Host{n}" for n in range(1, num_entries + 1)],
        "VM": [f"VM{n}" for n in range(1, num_entries + 1)],
        "Startup Status": np.random.choice(statuses, num_entries, p=[0.5, 0.3, 0.2])
    })
    sheets_data[f"Sheet{sheet_num}"] = df

# Plot pie charts for each sheet
num_sheets = len(sheets_data)
cols = 2
rows = (num_sheets + 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows))
axes = axes.flatten()

color_palettes = plt.cm.Set3.colors  # bright pastel colors

for i, (sheet_name, df) in enumerate(sheets_data.items()):
    status_counts = df["Startup Status"].value_counts()
    axes[i].pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=color_palettes[:len(status_counts)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    axes[i].set_title(f"{sheet_name} - Startup Status", fontsize=14)

# Hide unused axes if any
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()

# ✅ Save as JPG
plt.savefig("vm_startup_report.jpg", format="jpg", dpi=300)

plt.show()
