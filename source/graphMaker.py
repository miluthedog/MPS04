import matplotlib.pyplot as plt
import pandas as pd


class DataPlotter:
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

