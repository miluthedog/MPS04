import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# === Config ===
folder_path = 'source/data/AIfeatures'
csv_files = sorted(glob.glob(os.path.join(folder_path, '*.csv')))

# === PSD columns (assumed to be columns 3 to 28 = index 2 to 27) ===
psd_columns = [str(i) for i in range(1, 27)]  # '1' to '26'

# === Plot ===

for file in csv_files:
    df = pd.read_csv(file)
    psd_data = df[psd_columns].values.astype(float)
    mean_psd = psd_data.mean(axis=0)
    std_psd = psd_data.std(axis=0)
    label = os.path.splitext(os.path.basename(file))[0]

    x = range(1, 27)
    plt.plot(x, mean_psd, label=label)
    plt.fill_between(x, mean_psd - std_psd, mean_psd + std_psd, alpha=0.5)


plt.xlabel('Frequencies')
plt.ylabel('PSD')
plt.title('PSD distributions')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
