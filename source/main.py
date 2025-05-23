import sounddevice as sd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard
from scipy.signal import find_peaks, welch, detrend
from scipy.stats import skew, kurtosis
import tensorflow as tf
import os


class Collector:
    def __init__(self):
        plotRange = 661500 
        self.dataFrame = np.zeros(plotRange)
        self.plotter = LivePlot(plotRange)
        self.process = Processsor()

        self.samplerate = 44100
        self.blocksize = 4096

    def collect(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.dataFrame = indata[:, 0]
            self.plotter.updatePlot(self.dataFrame) # update plot

            self.process.updateCycle(indata[:, 0]) # update "processor"

        with sd.InputStream(samplerate=self.samplerate, blocksize=self.blocksize, channels=1, callback=callback):
            self.plotter.startPlot()
            while True:
                if keyboard.is_pressed('esc'):
                    break
                sd.sleep(100)


class Processsor:
    def __init__(self):
        self.model = tf.keras.models.load_model("model.keras")
        self.cycle = []
        self.lastPrediction = 0

        self.gripHeight = 0.15
        self.dropHeight = 0.03
        self.downsample = 20
        self.threshold = 0.002

    def peaks(self, signal, height):
        peaks, _ = find_peaks(np.abs(signal), height=height)
        return np.array(peaks)

    def updateCycle(self, signal):
        if len(self.cycle) < 10000:
            peaks = self.peaks(signal, self.gripHeight)
            if len(peaks) > 0:
                self.cycle = signal[peaks[-1]:]
                print(f"Cycle start, length: {len(self.cycle)}")
            elif len(self.cycle) > 0:
                self.cycle = np.append(self.cycle, signal)
                print(f"Collecting, length: {len(self.cycle)}")

        elif len(self.cycle) < 570000:
            self.cycle = np.append(self.cycle, signal)
            print(f"Collecting, length: {len(self.cycle)}")

        elif len(self.cycle) < 620000:
            peaks = self.peaks(signal, self.dropHeight)
            if len(peaks) > 0:
                self.cycle = signal[:peaks[0]]
                data = self.calculateFeatures(self.cycle)
                print(self.prediction(data))
                self.cycle = []
        else:
            print(f"Error: cycle not stop, length: {len(self.cycle)}")
            self.cycle = []

    def preprocessClip(self, signal):
        signal = signal[::self.downsample]
        signal = detrend(signal)
        signal = np.clip(signal, -self.threshold, self.threshold)
        return signal
    
    def preprocessRemove(self, signal):
        signal = signal[::self.downsample]
        signal = detrend(signal)
        signal = signal[np.abs(signal) <= self.threshold]
        return signal
  
    def calculateFeatures(self, signal):
        print("Cycle stop, calculating features...")
        
        signal = self.preprocessClip(signal)
        _, psd = welch(signal, fs=44100//self.downsample, nperseg=1024//self.downsample)

        psd_list = psd.tolist()
        if len(psd_list) < 26:
            psd_list += [0.0] * (26 - len(psd_list))
        else:
            psd_list = psd_list[:26]

        row = [kurtosis(self.preprocessRemove(signal)), skew(self.preprocessRemove(signal))] + psd.tolist()
        print(row)
        return row

    def prediction(self, data):
        sk = np.array(data[:2]).reshape(1, -1)
        psd = np.array(data[2:30]).reshape(1, -1)

        X = np.hstack((psd, sk))

        prediction = int((self.model.predict(X, verbose=0) > 0.5).astype(int)[0][0])

        if prediction == 0:
            print("Normal states")
        elif prediction == 1:
            print("Abnormal states")
            if self.lastPrediction == 1:
                print("Error: bolt lossen, sending message...")
                Message().send()

        self.lastPrediction = prediction


class Message:
    def __init__(self):
        pass

    def send(self):
        pass


class LivePlot:
    def __init__(self, plotRange):
        self.data = np.zeros(plotRange)
        self.line, = plt.plot(np.arange(plotRange), self.data)

        plt.xlim(0, plotRange)
        plt.ylim(-0.2, 0.2)

        plt.title("Live signal")
        plt.xlabel('ID')
        plt.ylabel('Amplitude')

    def updatePlot(self, updatedData):
        self.data = np.roll(self.data, -len(updatedData))
        self.data[-len(updatedData):] = updatedData
        self.line.set_ydata(self.data)

    def startPlot(self):
        self.ani = animation.FuncAnimation(plt.gcf(), lambda frame:(self.line,), interval=30, cache_frame_data=False)
        plt.show()


if __name__ == "__main__":
    Collector().collect()