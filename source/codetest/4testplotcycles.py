import pandas as pd
import matplotlib.pyplot as plt


class Plot:
    def __init__(self):
        self.filename = "data"

    def plot4(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}.csv")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            print (f"Cycle {i+1}: {len(data[data.columns[i]].dropna())}")
            axes[i].plot(data[data.columns[i]])
            axes[i].set_title(f"Cycle: {data.columns[i]}")
            axes[i].set_ylim(-0.1, 0.1)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Plot().plot4()
