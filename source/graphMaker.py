import matplotlib.pyplot as plt
import pandas as pd


class DataPlotter:
    def __init__(self, title=None):
        self.title = title

    def plot1(self, filename):
        filepath = f"source/data/{filename}"
        data = pd.read_csv(filepath)

        plt.plot(data.index, data[data.columns[1]])
        plt.title(self.title)
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.grid()
        plt.show()

    def plot4in1(self, filenames):
        for filename in filenames:
            filepath = f"source/data/{filename}"
            data = pd.read_csv(filepath)

            plt.plot(data.index, data[data.columns[1]])
        plt.title(self.title)
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.grid()
        plt.show()

    def plot4(self, filenames):
        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i, filename in enumerate(filenames):    
            filepath = f"source/data/{filename}"
            data = pd.read_csv(filepath)

            axes[i].plot(data.index, data[data.columns[1]])
            axes[i].set_xlabel(data.columns[0])
            axes[i].set_ylabel(data.columns[1])
            axes[i].grid()
        plt.suptitle(self.title)
        plt.tight_layout()
        plt.show()

