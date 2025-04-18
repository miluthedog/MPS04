import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''
Signal analysis:
Vibration appear when moving, slightly higher amplitude when accelerate
Amplitude ~0.2 at "grip"
Amplitude ~0.05 at "stop right trans"
Amplitude ~0.05 at "drop"
'''

class LivePlot:
    def __init__(self, plotRange):
        self.data = np.zeros(plotRange)
        self.line, = plt.plot(np.arange(plotRange), self.data)

        plt.xlim(0, plotRange)
        plt.ylim(-0.5, 0.5)
        plt.title("Live signal")
        plt.xlabel('ID')
        plt.ylabel('Amplitude')

    def update(self, updatedData):
        self.data = np.roll(self.data, -len(updatedData))
        self.data[-len(updatedData):] = updatedData
        self.line.set_ydata(self.data)

    def start(self):
        self.ani = animation.FuncAnimation(plt.gcf(), lambda frame:(self.line,), interval=30, cache_frame_data=False)
        plt.show()


class Collector:
    def __init__(self, plotRange=441000):
        self.dataFrame = np.zeros(plotRange)
        self.plotter = LivePlot(plotRange)

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