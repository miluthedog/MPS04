import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

'''
Largest signal: Grip
Second largest signal: Drop
=> Split from Grip to Drop (No reasonable delay)
'''

class Plot:
    def __init__(self):
        pass

    def plotdata(self, filename):
        data = pd.read_csv(f"source/data/{filename}.csv")
        plt.plot(data)
        plt.ylim(-0.5, 0.5)

        plt.title("Test signal")
        plt.xlabel("ID")
        plt.ylabel("Amplitude")
        
        plt.show()


if __name__ == "__main__":
    filename = "data"
    Plot().plotdata(filename)
