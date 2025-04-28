import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

'''
Cycle length: white ~590000 black ~ 510000 ()
black right motion 180000-410000
white right motion 180000-490000
'''

class FFT:
    def __init__(self):
        self.filename = "cycbbbb2.csv"
        #self.range = (150_000,180_000)
        #self.range = (0,300_000)
        self.range = (180_000, 410_000)
        #self.range = (180_000, 490_000)
        self.cycleID = 3

        self.frequency = 44100/10
    def fft(self, data):
        n = len(data)
        fft_result = fft(data)

        # Frequency values corresponding to the FFT results
        freqs = fftfreq(n, d=1/self.frequency)

        # Take only the positive frequencies and corresponding FFT values
        pos_freqs = freqs[:n//2]
        pos_fft_values = np.abs(fft_result)[:n//2]  # Amplitude of FFT

        return pos_freqs, pos_fft_values

    def extract(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        cycleData = data[data.columns[self.cycleID]].dropna()

        cycle = cycleData[self.range[0]:self.range[1]]
        cycle = cycle[::10]
        freqs, fft_values = self.fft(cycle)

        plt.plot(freqs, fft_values, color='r', label="FFT")
        plt.title(f"Cycle {self.cycleID+1}: {data.columns[self.cycleID]}")
        plt.ylim(-0.1, 0.1)

        plt.show()


if __name__ == "__main__":
    FFT().extract()