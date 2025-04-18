import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Plot:
    def __init__(self):
        pass

    def plotdata(self, filename, samplerate=44100):
        data = pd.read_csv(f"source/data/{filename}.csv").iloc[:,0]
        time = np.arange(len(data)) / samplerate
        plt.plot(time, data)
        plt.title("Test signal")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.ylim(-0.5, 0.5)
        plt.show()

Plot().plotdata("E1bwbw1", samplerate=44100)
