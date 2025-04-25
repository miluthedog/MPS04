import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

'''
Largest signal: Grip > 0.2
Second largest signal: Drop > 0.03
Third largest signal: Left accelerate > 0.03
Fourth largest signal: Upward accelerate (gripped) > 0.015 
Others are noised
'''

class Plot:
    def __init__(self):
        pass

    def plotdata(self, filename):
        data = pd.read_csv(f"source/data/{filename}.csv")
        plt.plot(data)
        plt.ylim(-0.1, 0.1)

        plt.title("Test signal")
        plt.xlabel("ID")
        plt.ylabel("Amplitude")
        
        plt.show()


if __name__ == "__main__":
    filename = "bbbb1"
    Plot().plotdata(filename)
