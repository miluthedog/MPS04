import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

'''
Workflow:
Cycle start: Find all isolated peaks > 0.15 (choose last point)
Choose cycle with ID
Cycle end: Find all isolated peaks > 0.03 (choose first point that far from its start)
'''

class Split:
    def __init__(self):
        self.filename = "data.csv"
        self.peakDis = 10000
        self.gripHeight = 0.15
        self.dropHeight = 0.03
        self.peakID = 0

    def firstPeaks(self, signal): # return all isolated first peaks
        peaks, _ = find_peaks(np.abs(signal), height=self.dropHeight)

        selected = [peaks[0]]
        for p in peaks[1:]:
            if p - selected[-1] > self.peakDis:
                selected.append(p)
        return np.array(selected)
    
    def lastPeaks(self, signal): # return all isolated last peaks
        peaks, _ = find_peaks(np.abs(signal), height=self.gripHeight)

        selected = [peaks[0]]
        for peak in peaks[1:]:
            if peak - selected[-1] > self.peakDis:
                selected.append(peak)
            else:
                selected[-1] = peak
        return np.array(selected)

    def splitcycle(self):
        data = pd.read_csv(f"source/data/{self.filename}")
        signal = data["Amplitude"].values
            # Find all cycle starts
        gripPeaks = self.lastPeaks(signal)
        gripID = gripPeaks[self.peakID]
        signal = signal[gripID:]
        print(f"Cycle starts: {gripPeaks} - ID {self.peakID}: {gripID}")
            # Find all cycle ends (choose the first that far from its start)
        dropPeaks = self.firstPeaks(signal)
        for id in dropPeaks:
            if id > 400000:
                dropID = id
                break
        signal = signal[:dropID]
        print(f"Cycle length: {dropID}")

        plt.plot(signal)
        plt.ylim(-0.1, 0.1)
        plt.axhline(y=self.gripHeight, color='r', alpha=0.3)
        plt.axhline(y=-self.gripHeight, color='r', alpha=0.3)
        plt.axhline(y=self.dropHeight, color='r', linestyle="--", alpha=0.3)
        plt.axhline(y=-self.dropHeight, color='r', linestyle="--", alpha=0.3)

        plt.title("Test cycle")
        plt.xlabel("ID")
        plt.ylabel("Amplitude")
        plt.show()


if __name__ == "__main__":
    Split().splitcycle()
