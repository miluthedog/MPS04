from sqlalchemy import create_engine
import sounddevice as sd

class Collector:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+pymysql://{"root"}:{"mps2024"}@{"mps2024"}@{"localhost"}:{3306}/{"iot_data"}")

    def collect(self):
        '''
        main==name:
        read data from sensor
        plot all data
        process data
        save processed data

        called:
        read (call process)
        '''