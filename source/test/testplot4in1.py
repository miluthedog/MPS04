import pandas as pd
import matplotlib.pyplot as plt


class Plot:
    def __init__(self):
        pass

    def plot4in1(self, filenames):
        for filename in filenames:
            data = pd.read_csv(f"source/data/{filename}.csv")
            plt.plot(data)
        plt.title("Test plot 4 in 1")
        plt.xlabel("ID")
        plt.ylabel(data.columns[0])
        plt.show()


if __name__ == "__main__":

    filenames = ['sample4black1', 'sample4white1', 'sampleHERRORwbwb1', 'sampleVERRORbwbw1']
    Plot().plot4in1(filenames)