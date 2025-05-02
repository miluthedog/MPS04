import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, norm, skew, kurtosis
from scipy.signal import detrend


class Extract:
    def __init__(self):
        self.filename = "data.csv"
        self.downsamplingRate = 10
        self.threshold = 0.002

    def preprocess(self, signal):
        signal = signal[::self.downsamplingRate]
        signal = detrend(signal)
        signal = signal[np.abs(signal) <= self.threshold]
        return signal

    def distributions(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}")
        results = []

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i, column in enumerate(data.columns[:4]):
            values = self.preprocess(data[column].dropna())
            print(f"Processing cycle {i+1}: {len(values)} data points")

            x = np.linspace(values.min(), values.max(), 1000)
            kde = gaussian_kde(values)
            mu, std = np.mean(values), np.std(values)

            signal_skew = skew(values)
            signal_kurtosis = kurtosis(values)
            
            results.append({
                'Cycle': data.columns[i],
                'Skewness': signal_skew,
                'Kurtosis': signal_kurtosis})

                # Histogram
            axes[i].hist(values, bins=30, alpha=0.7, color='skyblue', density=True)
                # KDE line
            axes[i].plot(x, kde(x), 'r-', linewidth=2)
                # Normal distribution line
            axes[i].plot(x, norm.pdf(x, mu, std), 'g--', linewidth=2)

            axes[i].set_title(f"Distribution: {column}")
            axes[i].set_xlabel("Value")
            axes[i].set_ylabel("Density")

        resultsFrame = pd.DataFrame(results)
        print(resultsFrame)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Extract().distributions()
