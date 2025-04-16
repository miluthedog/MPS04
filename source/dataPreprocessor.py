import sounddevice as sd
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy.signal import resample_poly

from graphPlotter import Plot


class Collector:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:mps2024@localhost:3306/iot_data")

    def downSample(self, data, downSamplingRate):
        if downSamplingRate == 44100:
                return data
        else:
            downSampleFactor = int(44100 / downSamplingRate)
            downSampledData = resample_poly(data, down=downSampleFactor, up=1)
            return downSampledData

    def collect(self, downSampleRate=441):

        def callback(indata, frames, time, status):
            if status:
                print(status)
            

        with sd.InputStream(samplerate=44100, blocksize=1024, channels=1, callback=callback):
            input()


if __name__ == "__main__":
    data = Collector()
    data.collect()