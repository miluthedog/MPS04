import pandas as pd
import numpy as np
from scipy.signal import welch, detrend
from scipy.stats import skew, kurtosis
import os

class FeatureSaver:
    def __init__(self):
        self.source_file = "source/data/cycE2wwww1.csv"
        self.save_file = "features.csv"
        self.downsample = 10
        self.clip = 0.005
        self.label = 0

    def preprocess(self, signal):
        signal = signal[::self.downsample]
        signal = detrend(signal)
        signal = np.clip(signal, -self.clip, self.clip)
        return signal

    def extract_features(self):
        data = pd.read_csv(self.source_file)
        rows = []

        for column in data.columns[:4]:
            raw = data[column].dropna().values
            signal = self.preprocess(raw)

            _, psd = welch(signal, fs=44100//self.downsample, nperseg=1024//self.downsample)

            row = [self.label, kurtosis(signal), skew(signal)] + psd.tolist()
            rows.append(row)

        if rows:
            df = pd.DataFrame(rows)
            header = not os.path.exists(self.save_file)
            df.to_csv(self.save_file, mode='a', header=header, index=False)

if __name__ == "__main__":
    FeatureSaver().extract_features()
