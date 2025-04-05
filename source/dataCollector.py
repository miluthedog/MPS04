from sqlalchemy import create_engine
import sounddevice as sd

from dataPreprocessor import Preprocess
from graphMaker import DataPlotter


class Collector:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+pymysql://{"root"}:{"mps2024"}@{"mps2024"}@{"localhost"}:{3306}/{"iot_data"}")

        self.channel = 1
        self.originalSamplingRate = 44100
        self.dataFrame = []
    
    def collect(self, samplingRate):
        def stopFrame():
            # if plc say stop, return true
            return False

        def callback(indata, frames, time, status):
            if status:
                print(f"Collecting error: {status}")
            downSampledData = Preprocess().downSample(indata, self.originalSamplingRate, samplingRate)
            self.dataFrame.append(downSampledData)

        try:
            with sd.InputStream(samplerate=self.originalSamplingRate, channels=self.channel, callback=callback):
                while not stopFrame():
                    sd.sleep(500)

        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    Collector().collect(44100)
    if Collector().dataFrame:
        DataPlotter("Raw data").plotdata(Collector().dataFrame)