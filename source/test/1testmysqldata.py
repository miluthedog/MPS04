import sounddevice as sd
import pandas as pd
import keyboard
from sqlalchemy import create_engine

'''
Data lost at ~1700 Hz (My sql "input overflow")
'''

class CollectorSQL:
    def __init__(self, engine):
        self.engine = create_engine(engine)

    def collect(self):

        def callback(indata, frames, time, status):
            if status:
                print(status)
            #dataFrame = pd.DataFrame({"Amplitude": indata[:, 0]}) # samplerate 44100
            #dataFrame = pd.DataFrame({"Amplitude": indata[::25, 0]}) # downsample to 1764
            dataFrame = pd.DataFrame({"Amplitude": indata[::100, 0]}) # downsample to 441
            dataFrame.to_sql("thuthap", con=self.engine, if_exists="append", index=False)

        with sd.InputStream(samplerate=44100, channels=1, callback=callback):
            while True:
                if keyboard.is_pressed('esc'):
                    break
                sd.sleep(100)


if __name__ == "__main__":
    data = CollectorSQL("mysql+pymysql://root:mps2024@localhost:3306/iot_data")
    data.collect()