import csv
import sys
import time

import keyboard
import sounddevice as sd

# Thiết lập thông số ghi dữ liệu
original_sample_rate = 44100
target_sample_rate = 441
channels = 1  # Số kênh âm thanh (mono)
downsample_factor = int(original_sample_rate / target_sample_rate)  # Hệ số giảm mẫu

# Đường dẫn đến file CSV
csv_filename = "C:/Users/User/Desktop/trainingAI/loi2vantietluu2.csv"

# Mở file CSV và thiết lập tiêu đề cột
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Amplitude"])  # Tiêu đề cột

    print("Bắt đầu ghi dữ liệu từ cảm biến. Nhấn phím Space để dừng...")

    # Hàm callback để thu thập dữ liệu âm thanh
    def callback(indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        # Lấy giá trị biên độ và chỉ giữ lại mỗi downsample_factor mẫu
        downsampled_data = indata[::downsample_factor, 0]
        for amplitude in downsampled_data:
            writer.writerow([amplitude])

    # Khởi tạo stream thu âm với tần số mẫu gốc (44100 Hz)
    with sd.InputStream(samplerate=original_sample_rate, channels=channels, callback=callback):
        while True:
            # Kiểm tra nếu phím Space được nhấn
            if keyboard.is_pressed('space'):
                print("Đã nhấn phím Space, dừng ghi dữ liệu.")
                break
            time.sleep(0.05)  # Giảm thời gian chờ để phản hồi nhanh hơn

print(f"Dữ liệu đã được lưu vào {csv_filename}")
