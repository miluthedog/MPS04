import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os


class Distribution:
    def __init__(self):
        self.filenames = ["horiBolt", "normal", "rotateBolt", "vertiBolt"]

# === Config ===
folder_path = 'source/data/AIfeatures'
csv_files = sorted(glob.glob(os.path.join(folder_path, '*.csv')))
value_key = 'Kurtosis'

# === Collect values ===
results = []
for file in csv_files:
    df = pd.read_csv(file)
    values = df[value_key].values
    mean_val = values.mean()
    std_val = values.std()
    label = os.path.splitext(os.path.basename(file))[0]
    results.append({
        'label': label,
        'mean': mean_val,
        'std': std_val,
        'values': values
    })


# === Plot ===
x_pos = np.arange(len(results))

# Plot individual values (hollow dots)
for i, r in enumerate(results):
    plt.plot([i]*len(r['values']), r['values'], 'o', markerfacecolor='none', markeredgecolor='blue', alpha=0.6)

# Plot error bars (mean ± std)
means = [r['mean'] for r in results]
stds = [r['std'] for r in results]
plt.errorbar(x_pos, means, yerr=stds, fmt='s', color='blue', capsize=4, linestyle='dotted', label='Mean ± STD')

# Connect means
plt.plot(x_pos, means, linestyle='dotted', color='blue')

# X-axis labels
labels = [r['label'] for r in results]
plt.xticks(x_pos, labels, rotation=45)
plt.ylabel(f'{value_key}')
plt.title(f'{value_key}')
plt.grid(True)
plt.tight_layout()
plt.show()
