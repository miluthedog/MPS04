from scipy.signal import resample_poly

from dataCollector import Collector
from graphMaker import DataPlotter


class Preprocessor():
    def __init__(self):
        pass

        def downSample(self, data, originalSamplingRate, downSamplingRate):
            if originalSamplingRate == downSamplingRate:
                return data
            else:
                downsampling_factor = int(originalSamplingRate / downSamplingRate)
                downSampledData = resample_poly(data, down=downsampling_factor, up=1)
                print(f"Checkpoint 1: Read {len(downSampledData)} signals")
                return downSampledData

    def splitCycle(self, data):
        cyclesData = data
        print(f"Checkpoint 2: Splitted {len(cyclesData)} cycles from the signal.")
        return cyclesData


if __name__ == "__main__":
    Collector().collect(44100)
    if Collector().dataFrame:
        cyclesData = Preprocessor().splitCycle(Collector().dataFrame)
        DataPlotter("Cycle").plotdata(cyclesData)