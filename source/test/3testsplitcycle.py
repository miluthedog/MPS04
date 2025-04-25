import pandas as pd
import numpy as np
from scipy.signal import find_peaks


class Split:
    def __init__(self):
        self.filename = "bbbb1"
        self.peakDis = 10000
        self.gripHeight = 0.2
        self.dropHeight = 0.03
        self.peakID = 1

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
        data = pd.read_csv(f"source/data/{self.filename}.csv")
        signal = data["Amplitude"].values

        gripPeaks = self.lastPeaks(signal)
        gripID = gripPeaks[self.peakID]
        signal = signal[gripID:]

        dropPeaks = self.firstPeaks(signal)
        for id in dropPeaks:
            if id > 400000:
                dropID = id
                break
        signal = signal[:dropID]

        dataFrame = pd.DataFrame({"Amplitude": signal})
        dataFrame.to_csv("cycle.csv", index=False)


if __name__ == "__main__":
    Split().splitcycle()
