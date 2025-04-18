from scipy.signal import find_peaks, welch, medfilt
import pandas as pd


class Processor:
    def __init__(self, filename):
        self.filename = f"source/data/{filename}.csv"

    def process(self):
        data = pd.read_csv(self.filename)
        signal = data["Amplitude"].values

        