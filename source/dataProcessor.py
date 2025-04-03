import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, welch, medfilt
from scipy import stats

class DataProcessor:
    def __init__(self):
        pass

    def process(self, data):
        features = [
            self.skew(data)]
        return features
    
    def skew(self):
        pass