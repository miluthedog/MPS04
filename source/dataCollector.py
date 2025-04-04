from sqlalchemy import create_engine
import sounddevice as sd

from dataPreprocessor import Preprocess


class Collector:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+pymysql://{"root"}:{"mps2024"}@{"mps2024"}@{"localhost"}:{3306}/{"iot_data"}")

        self.channel = 1
        self.originalSamplingRate = 44100
    
    def collect(self, samplingRate):
        