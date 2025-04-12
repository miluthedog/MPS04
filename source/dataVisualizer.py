import sounddevice as sd
import numpy as np
from graphPlotter import LivePlot


class Visualize:
    def __init__(self, plotRange):
        self.dataFrame = np.zeros(plotRange)
        self.plotter = LivePlot("Real-time raw data", plotRange)

    def collect(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.dataFrame = indata[:, 0]
            self.plotter.update(self.dataFrame)

        with sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=1024):
            self.plotter.start()
            sd.sleep(100)

if __name__ == "__main__":
    audio_stream = Visualize(plotRange=441000)
    audio_stream.collect()