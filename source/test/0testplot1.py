import matplotlib.pyplot as plt
import pandas as pd


class Plot:
    def __init__(self):
        pass

    def plotdata(self, filename):
        data = pd.read_csv(f"source/data/{filename}.csv")
        plt.plot(data)

        plt.title("Test signal")
        plt.xlabel("ID")
        plt.ylabel(data.columns[0])
        plt.ylim(-0.5, 0.5)
        plt.show()


Plot().plotdata("bbbb1")
