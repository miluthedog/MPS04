import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Processor:
    def __init__(self, filename, fs=44100):
        self.filename = f"source/data/{filename}.csv"
        self.fs = fs  # Sampling rate in Hz

    def process(self, window_ms=1):
        signal = pd.read_csv(self.filename)["Amplitude"].values
        total_samples = len(signal)

        # Convert window size in ms to samples
        window_size = int(self.fs * window_ms / 1000)

        # Compute RMS using non-overlapping windows
        rms_values = [
            np.sqrt(np.mean(signal[i:i+window_size]**2))
            for i in range(0, total_samples - window_size, window_size)
        ]

        # Time axes
        t_signal = np.arange(total_samples) / self.fs
        t_rms = np.arange(len(rms_values)) * (window_size / self.fs)

        # Plot both
        plt.figure(figsize=(10, 5))
        plt.plot(t_signal, signal, label="Original Signal", alpha=0.5)
        plt.plot(t_rms, rms_values, label=f"RMS ({window_ms}ms)", color="red", linewidth=2)
        plt.ylim(-0.5, 0.5)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude / RMS")
        plt.title("Signal and RMS Over Time")
        plt.legend()
        plt.tight_layout()
        plt.show()

        return rms_values

p = Processor("E1bwbw1")
p.process(window_ms=1)
