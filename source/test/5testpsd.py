import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, detrend

'''
Down sample (experimentally)
Detrend
Clip extreme value (Keep properties)
'''

class Extract:
    def __init__(self):
        self.filename = "data.csv"
        self.dowsamplingRate = 10
        self.clip = 0.005

    def preprocess(self, signal):
        signal = signal[::self.dowsamplingRate]
        signal = detrend(signal)
        signal = np.clip(signal, -self.clip, self.clip)
        return signal

    def psd(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            rawsignal = data[data.columns[i]].dropna()
            signal = self.preprocess(rawsignal)
            
            f, psd = welch(signal, fs=44100//self.dowsamplingRate, nperseg=1024//self.dowsamplingRate)

            print(f"Cycle {i+1}: {len(signal)} data points")
            axes[i].plot(f, psd)
            axes[i].set_title(f"Cycle: {data.columns[i]} - PSD")
            axes[i].set_xlabel("Frequency (Hz)")
            axes[i].set_ylabel("Power Spectral Density (PSD)")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Extract().psd()