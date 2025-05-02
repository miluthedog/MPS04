import sounddevice as sd
import pandas as pd
import keyboard


class Collector:
    def __init__(self):
        self.filename = "data.csv"
        self.data = []

    def collect(self):

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.data.extend(indata[:, 0])

        with sd.InputStream(samplerate=44100, channels=1, callback=callback):
            while True:
                if keyboard.is_pressed('esc'):
                    break
                sd.sleep(100)

        dataFrame = pd.DataFrame({"Amplitude": self.data})
        dataFrame.to_csv(self.filename, index=False)


if __name__ == "__main__":
    Collector().collect()