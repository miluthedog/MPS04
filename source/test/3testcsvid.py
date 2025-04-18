import pandas as pd

class Plot:
    def get_positions(self, filename, threshold):
        d = pd.read_csv(f"source/data/{filename}.csv").iloc[:,0]
        return d[d > threshold].index.tolist()

# Example
pos = Plot().get_positions("bbbb1", 0.1)
print(pos)
