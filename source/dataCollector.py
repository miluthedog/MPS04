import sounddevice as sd
import numpy as np

from graphPlotter import LivePlot


class Collector:
    def __init__(self, plotRange):
        self.dataFrame = np.zeros(plotRange)
        self.plotter = LivePlot("Real-time raw data", plotRange)

    def collect(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.dataFrame = indata[:, 0]
            self.plotter.update(self.dataFrame)

        with sd.InputStream(samplerate=44100, blocksize=1024, channels=1, callback=callback):
            self.plotter.start()
            sd.sleep(100)


if __name__ == "__main__":
    data = Collector(plotRange=441000)
    data.collect()