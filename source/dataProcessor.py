import numpy as np
from scipy.signal import find_peaks, welch
from scipy import stats

from dataCollector import Collector
from dataPreprocessor import Preprocessor
from graphMaker import DataPlotter


class Processor:
    def __init__(self):
        pass

    def process(self, data, fs=1.0):
        """
        Process the signal data to extract time-domain and frequency-domain features.
        
        :param data: The signal data (1D array-like)
        :param fs: Sampling frequency (default is 1.0)
        :return: A list of extracted features
        """
        features = [
            # Time-domain features
            self.mean(data),
            self.variance(data),
            self.skew(data),
            self.kurtosis(data),
            self.rmse(data),
            self.max(data),
            self.min(data),
            self.zero_crossings(data),
            self.median(data),
            
            # Frequency-domain features
            *self.frequency_features(data, fs)
        ]
        return features
    
    # Time-domain features
    def mean(self, data):
        return np.mean(data)

    def variance(self, data):
        return np.var(data)

    def skew(self, data):
        return stats.skew(data)

    def kurtosis(self, data):
        return stats.kurtosis(data)

    def rmse(self, data):
        return np.sqrt(np.mean(np.square(data)))

    def max(self, data):
        return np.max(data)

    def min(self, data):
        return np.min(data)

    def zero_crossings(self, data):
        # Count the number of zero-crossings in the data
        zero_crossings = np.where(np.diff(np.sign(data)))[0]
        return len(zero_crossings)

    def median(self, data):
        return np.median(data)
    
    # Frequency-domain features
    def frequency_features(self, data, fs):
        # Compute power spectral density (PSD) using Welch's method
        f, Pxx = welch(data, fs=fs, nperseg=1024)
        
        # Compute the peak frequency
        peak_freqs, _ = find_peaks(Pxx)
        peak_frequency = f[peak_freqs][np.argmax(Pxx[peak_freqs])] if peak_freqs.size > 0 else 0
        
        # Total power
        total_power = np.sum(Pxx)
        
        # Frequency band power (e.g., low and high frequency)
        low_band_power = np.sum(Pxx[(f >= 0) & (f <= 4)])  # Example: delta band (0-4 Hz)
        high_band_power = np.sum(Pxx[(f > 30) & (f <= 100)])  # Example: beta band (30-100 Hz)
        
        # Spectral entropy (a measure of the complexity of the spectrum)
        spectral_entropy = -np.sum(Pxx * np.log(Pxx + np.finfo(float).eps))  # Avoid log(0) errors

        return [
            total_power,
            peak_frequency,
            low_band_power,
            high_band_power,
            spectral_entropy
        ]


if "__main__" == __name__:
    Collector().collect(44100)
    if Collector().dataFrame:
        cyclesData = Preprocessor().splitCycle(Collector().dataFrame)
        features = Processor().process(cyclesData)
        # save to csv