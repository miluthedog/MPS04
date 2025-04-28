import pandas as pd
import numpy as np
from scipy.signal import welch
from scipy.signal.windows import hann

class PSDExtractor:
    def __init__(self):
        self.filename = "cycE2wbwb1.csv"
        #self.range = (150_000,180_000)
        #self.range = (0,300_000)
        self.range = (200_000, 300_000)
        #self.range = (180_000, 490_000)
        self.cycleID = 3
        self.downsample_rate = 10

        self.Fs = 44100 / 10  # Your sampling frequency after downsampling (Fs)
        self.numWindows = 8

    def nextpow2(self, n):
        return int(np.ceil(np.log2(n)))

    def compute_psd(self, data):
        nfft = 2 ** self.nextpow2(len(data))
        nWin = nfft // self.numWindows
        noverlap = nWin // 2
        window = hann(nWin)

        freqs, pxx = welch(
            data, 
            fs=self.Fs, 
            window=window, 
            nperseg=nWin, 
            noverlap=noverlap, 
            nfft=nfft,
            scaling='density'
        )

        PdBWx = 10 * np.log10(pxx)
        return freqs, PdBWx

    def extract(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        cycleData = data[data.columns[self.cycleID]].dropna()
        cycle = cycleData[self.range[0]:self.range[1]]
        cycle = cycle[::self.downsample_rate]

        freqs, PdBWx = self.compute_psd(cycle)

        # Plot
        import matplotlib.pyplot as plt
        plt.plot(freqs, PdBWx, color='b')
        plt.title(f"PSD of Cycle {self.cycleID+1}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("PSD (dB/Hz)")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    PSDExtractor().extract()
