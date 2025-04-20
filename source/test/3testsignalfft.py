import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

signal = pd.read_csv(f"source/data/wwww1.csv")["Amplitude"].values

fs = 44100  # Hz

# Step 1: DC Offset removal
signal_no_dc = signal - np.mean(signal)
print("Mean after DC removal:", np.mean(signal_no_dc))

# Step 2: Windowing
window = np.hamming(len(signal_no_dc))
signal_windowed = signal_no_dc * window

# Step 3: FFT
fft = np.fft.fft(signal_windowed)
fft_mag = np.abs(fft) / len(fft)  # Normalize
freqs = np.fft.fftfreq(len(fft), 1/fs)

# Step 4: Positive frequencies only
half = len(freqs) // 2
fft_mag = fft_mag[:half]
freqs = freqs[:half]

# Step 5: Plot
plt.figure(figsize=(10, 4))
plt.plot(freqs, fft_mag, color='blue')
plt.title("Frequency Domain (FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.tight_layout()
plt.show()
