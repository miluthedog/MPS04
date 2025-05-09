import pandas as pd
import numpy as np
from scipy.signal import welch, detrend
from scipy.stats import skew, kurtosis
import os


class FeatureSaver:
    def __init__(self):
        self.filename = "data"
        self.output = "features.csv"

        self.downsample = 20
        self.threshold = 0.002
        self.label = 0

    def preprocessClip(self, signal):
        signal = signal[::self.downsample]
        signal = detrend(signal)
        signal = np.clip(signal, -self.threshold, self.threshold)
        return signal
    
    def preprocessRemove(self, signal):
        signal = signal[::self.downsample]
        signal = detrend(signal)
        signal = signal[np.abs(signal) <= self.threshold]
        return signal

    def extract_features(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}.csv")
        rows = []

        for column in data.columns[:4]:
            raw = data[column].dropna().values
            signal = self.preprocessClip(raw)

            _, psd = welch(signal, fs=44100//self.downsample, nperseg=1024//self.downsample)
            row = [self.label, kurtosis(self.preprocessRemove(signal)), skew(self.preprocessRemove(signal))] + psd.tolist()

            rows.append(row)

        if rows:
            dataFrame = pd.DataFrame(rows)
            header = not os.path.exists(self.output)
            dataFrame.to_csv(self.output, mode='a', header=header, index=False)

if __name__ == "__main__":
    FeatureSaver().extract_features()
