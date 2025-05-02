import pandas as pd
import matplotlib.pyplot as plt

'''
Operating state lengths seem equal
Idle state lengths not equal
'''

class Plot:
    def __init__(self):
        self.filename = "data.csv"

    def plot4(self):
        data = pd.read_csv(f"source/data/cyc/{self.filename}")

        for i in range(4):
            plt.plot(data[data.columns[i]])
        plt.title(f"Plot {self.filename}")
        plt.ylim(-0.05, 0.05)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Plot().plot4()
