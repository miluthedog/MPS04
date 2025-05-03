import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, detrend, butter, filtfilt

'''
Nyquist-Shannon Sampling Theorem:
Sampling frequency must be double the system frequency
Downsample requires low-pass filter and bandwidth limited (Unless using low frequency sensor)

Preprocess:
Power at 300 Hz is from shock data -> clip instead of remove
low pass filter: remove fold-back signal (more clear without clip)
'''

class Extract:
    def __init__(self):
        self.filename = "data.csv"
        self.downSamplingRate = 20
        self.downSamplingRateCompare = 20
        self.threshold = 0.005

    def preprocess(self, signal):
        signal = detrend(signal)
        signal = np.clip(signal, -self.threshold, self.threshold)
        signal = signal[::self.downSamplingRate]
        return signal

    def preprocessCompare(self, signal):
            # Detrend
        signal = detrend(signal)
            # Low pass filter
        b, a = butter(4, 1.8 / self.downSamplingRateCompare, btype='low')
        signal = filtfilt(b, a, signal)
            # Clip/Remove extreme value
        signal = np.clip(signal, -self.threshold, self.threshold)
        #signal = signal[np.abs(signal) <= self.threshold]
            # Down sampling
        signal = signal[::self.downSamplingRateCompare]
        return signal

    def psd(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            rawsignal = data[data.columns[i]].dropna()

            signal = self.preprocess(rawsignal)
            f, psd = welch(signal, fs=44100//self.downSamplingRate, nperseg=1024//self.downSamplingRate)
            print(f"Cycle {i+1}: {len(signal)} data points | nperseg: {1024//self.downSamplingRate} | {len(f)} frequency ")

            #signalCompare = self.preprocessCompare(rawsignal)
            #fCompare, psdCompare = welch(signalCompare, fs=44100//self.downSamplingRateCompare, nperseg=1024//self.downSamplingRateCompare)

            axes[i].plot(f, psd)
            #axes[i].plot(fCompare, psdCompare, ls = "--", color="r", alpha=0.5)

            axes[i].set_title(f"Cycle: {data.columns[i]} - PSD")
            axes[i].set_xlabel("Frequency (Hz)")
            axes[i].set_ylabel("Power Spectral Density (PSD)")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Extract().psd()