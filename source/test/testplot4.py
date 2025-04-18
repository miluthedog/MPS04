import pandas as pd
import matplotlib.pyplot as plt

class Plot:
    def __init__(self):
        pass

    def plot4(self, filenames):
        datas = [pd.read_csv(f"source/data/{filename}.csv") for filename in filenames]
        _, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i, data in enumerate(datas):    
            axes[i].plot(data)
            axes[i].set_xlabel("ID")
            axes[i].set_ylabel(data.columns[0])
            axes[i].set_ylim(-0.5, 0.5)

        plt.suptitle("Test 4 signal")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    filenames = ['sample4black1', 'sample4white1', 'sampleHERRORwbwb1', 'sampleVERRORbwbw1']
    Plot().plot4(filenames)