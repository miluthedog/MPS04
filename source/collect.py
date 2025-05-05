import sounddevice as sd
import pandas as pd
import numpy as np
import keyboard
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


class Collector:  # Collect and display data information
    def __init__(self):
        self.peakNumber = 4
        self.downSample = 1

        self.filename = "data.csv"
        self.data = []

    def peaks(self, threshold, signal):  # Detect isolated peaks
        peaks, _ = find_peaks(np.abs(signal), height=threshold)

        selected = [peaks[0]]
        for peak in peaks[1:]:
            if (peak - selected[-1]) > (10000 // self.downSample):
                selected.append(peak)
        return np.array(selected)

    def information(self):  # Display data informations
        print(f"Done collecting. Data length: {len(self.data)}")
        print(f"Min: {min(self.data)}, Max: {max(self.data)}, Mean: {np.mean(self.data)}")

        peaks10 = self.peaks(0.1, self.data)
        peaks15 = self.peaks(0.15, self.data)
        peaks20 = self.peaks(0.2, self.data)
        print(f"0.1 peaks: {peaks10}, 0.15 peaks: {peaks15}, 0.2 peaks: {peaks20}")

        for peak in [peaks10, peaks15, peaks20]:
            if len(peak) == self.peakNumber:
                selectedPeaks = peak
                break
        print(f"selected peaks: {selectedPeaks}")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()
        for index in range(self.peakNumber):
            startID = selectedPeaks[index]
            segment = self.data[startID:]

            endIDs = self.peaks(0.03, segment)
            endIDs = endIDs[endIDs > (400000 // self.downSample)]
            if len(endIDs) > 0:
                endID = endIDs[0]
            else:
                endID = len(segment)

            cycleSignal = segment[:endID]
            axes[index].plot(cycleSignal)
            axes[index].set_title(f"Cycle {index+1}")
            axes[index].set_ylim(-0.1, 0.1)
            print(f"Cycle {index+1} length: {endID}")
        plt.tight_layout()
        plt.show()

    def collect(self):  # Collect data
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.data.extend(indata[:, 0])

        with sd.InputStream(samplerate=(44100 // self.downSample), channels=1, callback=callback):
            while True:
                if keyboard.is_pressed('esc'):
                    break
                sd.sleep(100)

        dataFrame = pd.DataFrame({"Amplitude": self.data})
        dataFrame.to_csv(self.filename, index=False)

        self.information()


if __name__ == "__main__":
    Collector().collect()