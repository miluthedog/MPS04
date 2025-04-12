import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class LivePlot:
    def __init__(self, plotTitle=None, plotRange=441000):
        self.data = np.zeros(plotRange)
        self.line, = plt.plot(np.arange(plotRange), self.data)

        plt.xlim(0, plotRange)
        plt.ylim(-1, 1)
        plt.title = plotTitle
        plt.xlabel('ID')
        plt.ylabel('Amplitude')

    def update(self, updatedData):
        self.data = np.roll(self.data, -len(updatedData))
        self.data[-len(updatedData):] = updatedData
        self.line.set_ydata(self.data)

    def start(self):
        self.ani = animation.FuncAnimation(plt.gcf(), lambda frame:(self.line,), interval=30, cache_frame_data=False)
        plt.show()


class Plot:
    def __init__(self, title=None):
        self.title = title

    def plotdata(self, data):
        plt.plot(data)
        plt.title(self.title)
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.grid()
        plt.show()

    def plot4in1(self, datas):
        for data in datas:
            plt.plot(data)
        plt.title(self.title)
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.grid()
        plt.show()

    def plot4(self, datas):
        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i, data in enumerate(datas):    
            axes[i].plot(data)
            axes[i].set_xlabel(data.columns[0])
            axes[i].set_ylabel(data.columns[1])
            axes[i].grid()
        plt.suptitle(self.title)
        plt.tight_layout()
        plt.show()

