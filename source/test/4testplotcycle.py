import pandas as pd
import matplotlib.pyplot as plt


class Plot:
    def __init__(self):
        self.filename = "data.csv"

    def plot4(self):
        data = pd.read_csv(f"source/data/{self.filename}")

        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i in range(4):
            axes[i].plot(data[data.columns[i]])
            axes[i].set_title(f"Cycle: {data.columns[i]}")
            axes[i].set_ylim(-0.1, 0.1)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Plot().plot4()
