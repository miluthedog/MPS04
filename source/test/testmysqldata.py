import sounddevice as sd
import pandas as pd
from sqlalchemy import create_engine

'''
occurs "input overflow" or lost of data upload to db at ~1700 Hz
'''

class Collector:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:mps2024@localhost:3306/iot_data")

    def collect(self):

        def callback(indata, frames, time, status):
            if status:
                print(status)
            #dataFrame = pd.DataFrame({"Amplitude": indata[:, 0]}) # samplerate 44100
            #dataFrame = pd.DataFrame({"Amplitude": indata[::25, 0]}) # downsample to 1764
            dataFrame = pd.DataFrame({"Amplitude": indata[::100, 0]}) # downsample to 441
            dataFrame.to_sql("thuthap", con=self.engine, if_exists="append", index=False)

        with sd.InputStream(samplerate=44100, channels=1, callback=callback):
            input()


if __name__ == "__main__":
    data = Collector()
    data.collect()