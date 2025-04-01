import matplotlib.pyplot as plt
import pandas as pd


class DataPlotter:
    def __init__(self):
        self.figsize = (10, 8)

    def plot(self, filename):
        filepath = f"source/data/{filename}"

        df = pd.read_csv(filepath)
        
        x_label = df.columns[0]
        y_label = df.columns[1]
        
        # Create the plot
        plt.figure(figsize=self.figsize)
        plt.plot(df.index, df[df.columns[1]])
        plt.title(filename)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid()
        plt.show()

    def plotFour(self, filenames):
        _, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, filename in enumerate(filenames):    
            filepath = f"source/data/{filename}"

            df = pd.read_csv(filepath)
            
            x_label = df.columns[0]
            y_label = df.columns[1]

            axes[i].plot(df.index, df[df.columns[1]])
            axes[i].set_title(filename)
            axes[i].set_xlabel(x_label)
            axes[i].set_ylabel(y_label)
            axes[i].grid()
        
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    DataPlotter().plot("test.csv")
    #DataPlotter().plotFour(["test.csv", "test.csv", "test.csv", "test.csv"])
