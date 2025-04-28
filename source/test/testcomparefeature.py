import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis


class Compare:
    def __init__(self):
        self.filename = "cycwwww2.csv"
        self.rmswindow = 10000

    def extract(self, data):
        skewness = skew(data)
        kurt = kurtosis(data)
        rms = np.sqrt(np.mean(data**2))
        mean = np.mean(data)
        std = np.std(data)

        features =  {f"Skewness: {skewness}, Kurtosis: {kurt}, RMS: {rms}, Mean: {mean}, STD: {std}"}
        return features

    def RMS(self, data):
        return np.sqrt(pd.Series(data).rolling(self.rmswindow, center=True).mean())

    def feature(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            cycle = data[data.columns[i]].dropna()
            if len(cycle) > 600000:
                print(f"Cycle {i+1}: failed (length = {len(cycle)})")
                continue

            features = self.extract(cycle)
            print(f"Cycle {i+1}: {features}")

            axes[i].plot(cycle, alpha=0.5)
            axes[i].plot(self.RMS(cycle))
            axes[i].set_title(f"Cycle: {data.columns[i]}")
            axes[i].set_ylim(-0.1, 0.1)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    Compare().feature()