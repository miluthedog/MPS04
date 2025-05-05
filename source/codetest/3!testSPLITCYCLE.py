import pandas as pd
import numpy as np
from scipy.signal import find_peaks


class Split:
    def __init__(self):
        self.filename = "data.csv"
        self.peakNumber = 4
        self.labels = ["w", "w", "w", "w"] # Cycle label

        self.peakDis = 10000
        self.gripHeight = 0.15
        self.dropHeight = 0.03

    def firstPeaks(self, signal):
        peaks, _ = find_peaks(np.abs(signal), height=self.dropHeight)

        selected = [peaks[0]]
        for p in peaks[1:]:
            if p - selected[-1] > self.peakDis:
                selected.append(p)
        return np.array(selected)
    
    def lastPeaks(self, signal):
        peaks, _ = find_peaks(np.abs(signal), height=self.gripHeight)

        selected = [peaks[0]]
        for peak in peaks[1:]:
            if peak - selected[-1] > self.peakDis:
                selected.append(peak)
            else:
                selected[-1] = peak
        return np.array(selected)

    def splitcycle(self):
        data = pd.read_csv(f"source/data/raw/{self.filename}")
        signal = data["Amplitude"].values
        cycles = []

        gripPeaks = self.lastPeaks(signal)
        for peak in range(self.peakNumber):
            gripID = gripPeaks[peak]
            cycleSignal = signal[gripID:]

            dropPeaks = self.firstPeaks(cycleSignal)
            for id in dropPeaks:
                if id > 400000:
                    dropID = id
                    break
            cycleSignal = cycleSignal[:dropID]
            print(f"Cycle length: {dropID}")
            cycles.append(cycleSignal)

        dataFrame = pd.DataFrame(cycles).transpose()
        dataFrame.columns = self.labels
        dataFrame.to_csv("cycles.csv", index=False)


if __name__ == "__main__":
    Split().splitcycle()