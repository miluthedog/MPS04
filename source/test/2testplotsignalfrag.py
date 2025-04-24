import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

'''
Average cycle length ~13 sec (600000 signal at 44100 Hz)
50000-150000: Go up
150000-500000: Go right
500000-600000: Go down

Idle state amplitude < 0.00025 (If not apply vibration)
'''

class Plot:
    def __init__(self):
        pass

    def plot4(self, filename, plotRange):
        data = pd.read_csv(f"source/data/{filename}.csv")
        signal = data["Amplitude"].values

        peaks, _ = find_peaks(signal, height=0.1)
        gripID = peaks[0] if len(peaks) > 0 else 0
        signal = signal[gripID:]

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            start, end = plotRange[i]
            axes[i].plot(signal[start:end])
            if i == 0:
                axes[i].set_ylim(-0.05, 0.05)
            else:
                axes[i].set_ylim(-0.0025, 0.0025)
                axes[i].axhline(y=0.0002, color='r', alpha=0.3)
                axes[i].axhline(y=-0.0002, color='r', alpha=0.3)
            axes[i].set_title(f"Signal {start}-{end}")
            axes[i].set_xlabel("ID")
            axes[i].set_ylabel(f"Amplitude")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    filename = "E1bwbw1"
    plotRange = [(0, 1_000_000), (50_000, 150_000), (150_000, 500_000), (500_000, 600_000)]
    Plot().plot4(filename, plotRange)
