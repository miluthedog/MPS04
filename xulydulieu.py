import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, welch, medfilt
from scipy import stats

# Đọc dữ liệu từ file CSV
data = pd.read_csv("C:/Users/User/Desktop/trainingAI/loi2vantietluu2.csv")

# Giả sử tín hiệu nằm trong cột 'Amplitude' (đổi tên cột này thành tên đúng trong file của bạn)
signal = data['Amplitude'].values  # Cột chứa dữ liệu tín hiệu

# Hàm tính giá trị RMS cho một đoạn tín hiệu
def calculate_rms(signal_segment):
    return np.sqrt(np.mean(signal_segment**2))

# Kích thước cửa sổ cho việc tính RMS
window_size = 5

# Tạo danh sách để lưu giá trị RMS
rms_values = []

# Tính RMS cho từng đoạn tín hiệu với kích thước 'window_size'
for i in range(len(signal) - window_size + 1):
    window = signal[i:i + window_size]
    rms = calculate_rms(window)
    rms_values.append(rms)

# Chuyển danh sách giá trị RMS thành mảng numpy để tiện xử lý
rms_values = np.array(rms_values)

# Làm mượt tín hiệu RMS
filtered_rms = medfilt(rms_values, kernel_size=5)

# Tìm đỉnh trên tín hiệu RMS đã làm mượt
min_distance = 7200  # Khoảng cách tối thiểu giữa các đỉnh
peaks, _ = find_peaks(filtered_rms, height=0.01, distance=min_distance)

# Vẽ đồ thị so sánh tín hiệu gốc và tín hiệu RMS đã làm mượt
plt.figure(figsize=(9, 6))

# Đồ thị tín hiệu gốc
plt.subplot(3, 1, 1)
plt.plot(signal, label="Tín hiệu gốc")
plt.title("Tín hiệu ban đầu với nhiễu")
plt.legend()

# Đồ thị các đỉnh đã phát hiện
plt.subplot(3, 1, 3)
plt.plot(filtered_rms, label="Giá trị RMS", color='orange')
plt.plot(peaks, filtered_rms[peaks], "x", label="Đỉnh đã phát hiện", color='red')
plt.title("Đỉnh trong tín hiệu RMS")
plt.legend()

plt.tight_layout()
plt.show()

# Trích xuất các đặc trưng của từng chu kỳ
cycles = [signal[peaks[i]:peaks[i+1]] for i in range(len(peaks)-1)]
cycle_features = []

for cycle in cycles:
    # Độ dài chu kỳ
    cycle_length = len(cycle)

    # PSD của chu kỳ
    freqs, psd = welch(cycle)

    # Độ nhọn (kurtosis) và độ nghiêng (skewness)
    kurtosis = stats.kurtosis(cycle)
    skewness = stats.skew(cycle)

    # Trung bình và độ lệch chuẩn
    mean = np.mean(cycle)
    std_dev = np.std(cycle)

    # Tìm số lượng đỉnh vượt ngưỡng 0.1 trong chu kỳ
    peaks_in_cycle, _ = find_peaks(cycle, height=0.005, distance= 500)
    num_peaks_above_threshold = len(peaks_in_cycle)

    # Lưu trữ đặc trưng cho mỗi chu kỳ
    cycle_features.append({
        'length': cycle_length,
        'psd_mean': np.mean(psd),  # Lưu trung bình PSD
        'kurtosis': kurtosis,
        'skewness': skewness,
        'mean': mean,
        'std_dev': std_dev,
        'num_peaks_above_threshold': num_peaks_above_threshold  # Số lượng đỉnh vượt ngưỡng 0.1
    })

# Chuyển danh sách đặc trưng thành DataFrame
df = pd.DataFrame(cycle_features)

# Lưu đặc trưng vào file CSV
csv_filename = "C:/Users/User/Desktop/trainingAI/2loi2.csv"
df.to_csv(csv_filename, index=False)

print(f"Đặc trưng đã được lưu vào {csv_filename}")
