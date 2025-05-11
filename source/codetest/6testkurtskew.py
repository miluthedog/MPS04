import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os


class Distribution:
    def __init__(self):
        self.filenames = ["horiBolt", "normal", "rotateBolt", "vertiBolt"]
        self.col = "Kurtosis"
        #self.col = "Skewness"

    def cal(self):
        results = []
        for i, filename in enumerate(self.filenames):
            dataFrame = pd.read_csv(f"source/data/AIfeatures/{filename}.csv")
            values = dataFrame[self.col].values
            mean = values.mean()
            std = values.std()
            label = self.filenames[i]
            results.append({
                'label': label,
                'mean': mean,
                'std': std,
                'values': values})
        return results

    def plot(self):
        data = self.cal()

        for i, datapoint in enumerate(data):
            plt.plot([i]*len(datapoint['values']), datapoint['values'], 'o', markerfacecolor='none', markeredgecolor='blue', alpha=0.6)

        means = [datapoint['mean'] for datapoint in data]
        stds = [datapoint['std'] for datapoint in data]
        labels = [datapoint['label'] for datapoint in data]

        plt.errorbar(np.arange(len(data)), means, yerr=stds, fmt="s", color="blue", capsize=4, linestyle="dotted", label="Mean ± STD")

        plt.plot(np.arange(len(data)), means, linestyle="dotted", color="blue")

        plt.xticks(np.arange(len(data)), labels, rotation=45)
        plt.ylabel(self.col)
        plt.title(self.col)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Distribution().plot()