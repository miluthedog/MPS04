import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

class Compare:
    def __init__(self):
        self.filename = "cycbbbb2.csv"
        self.frequency = 44100  # Sampling frequency, no change

    def compute_fft(self, data):
        """
        Compute the Fast Fourier Transform (FFT) of the signal.

        Parameters:
            data: Signal data to compute the FFT of.

        Returns:
            freqs: Array of frequency values.
            fft_values: Array of FFT amplitude values.
        """
        # Perform FFT on the signal
        n = len(data)
        fft_result = fft(data)

        # Frequency values corresponding to the FFT results
        freqs = fftfreq(n, d=1/self.frequency)

        # Take only the positive frequencies and corresponding FFT values
        pos_freqs = freqs[:n//2]
        pos_fft_values = np.abs(fft_result)[:n//2]  # Amplitude of FFT

        return pos_freqs, pos_fft_values

    def feature(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        _, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i in range(4):
            cycle = data[data.columns[i]].dropna()
            if len(cycle) > 600000:
                print(f"Cycle {i+1}: failed (length = {len(cycle)})")
                continue

            # Compute FFT for the cycle
            freqs, fft_values = self.compute_fft(cycle)

            # Plot the time-domain signal and its FFT
            axes[i].plot(freqs, fft_values, color='r', label="FFT")
            axes[i].set_title(f"Cycle {i+1}: {data.columns[i]}")
            #axes[i].set_ylim(-0.1, 0.1)


        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    Compare().feature()
