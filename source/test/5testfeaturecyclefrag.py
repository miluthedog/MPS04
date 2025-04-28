import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

class FeatureExtractor:
    def __init__(self):
        self.filename = "cycbbbb2.csv"
        #self.range = (150_000,180_000)
        #self.range = (0,300_000)
        self.range = (250_000, 400_000)
        #self.range = (180_000, 490_000)
        self.cycleID = 3
        self.downsample_rate = 10

    def extract_features(self, data):
        features = {
            "mean": np.mean(data),
            "std": np.std(data),
            "rms": np.sqrt(np.mean(np.square(data))),
            "skew": skew(data),
            "kurtosis": kurtosis(data)
        }
        return features

    def extract(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        cycleData = data[data.columns[self.cycleID]].dropna()

        cycle = cycleData[self.range[0]:self.range[1]]
        #cycle = cycle[::self.downsample_rate]

        features = self.extract_features(cycle)

        for key, value in features.items():
            print(f"{key}: {value:.6f}")

if __name__ == "__main__":
    FeatureExtractor().extract()
