import sys
import threading
import time
from joblib import load

import keyboard
import numpy as np
import pandas as pd
import scipy.stats as stats
import sounddevice as sd
from scipy.signal import find_peaks, welch, medfilt
from sqlalchemy import create_engine
from sqlalchemy import text

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mps2024",
    "database": "iot_data",
    "port": 3306
}

# Kết nối đến MySQL
engine = create_engine(
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

# Thiết lập thông số ghi dữ liệu
original_sample_rate = 44100
target_sample_rate = 441
channels = 1  # Số kênh âm thanh (mono)
downsample_factor = int(original_sample_rate / target_sample_rate)  # Hệ số giảm mẫu

stop_event = threading.Event()


# Hàm ghi dữ liệu từ cảm biến và lưu vào MySQL
def calculate_rms(signal, window_size):
    rms_values = [
        np.sqrt(np.mean(signal[i:i + window_size] ** 2))
        for i in range(len(signal) - window_size + 1)
    ]
    return np.array(rms_values)

def record_data():
    print("Bắt đầu ghi dữ liệu từ cảm biến. Nhấn phím Space để dừng...")

    def callback(indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)

        # Chuyển đổi `downsampled_data` thành danh sách
        downsampled_data = list(indata[::downsample_factor, 0])


        # Tạo DataFrame với Amplitude và Timestamp
        df = pd.DataFrame({
            "Amplitude": downsampled_data,  # Dữ liệu Amplitude
        })

        # Lưu DataFrame vào MySQL
        df.to_sql("thuthap", con=engine, if_exists="append", index=False)
        df.to_sql("cbgt", con=engine, if_exists="append", index=False)
        #print("Dữ liệu đã được lưu vào MySQL.")

    # Sử dụng sounddevice để lấy dữ liệu từ cảm biến
    with sd.InputStream(samplerate=original_sample_rate, channels=channels, callback=callback):
        while not stop_event.is_set():
            time.sleep(0.5)

def save_data(df, engine):
    if not df.empty:
        try:
            print(f"Lưu vào bảng 'xuly' với dữ liệu:\n{df.head()}")  # In dữ liệu trước khi lưu
            df.to_sql("xuly", con=engine, if_exists="append", index=False)
            print("Đã lưu các bản ghi mới vào bảng 'xuly'.")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào bảng 'xuly': {e}")
    else:
        print("Không có bản ghi mới để lưu vào bảng 'xuly'.")



# Đọc dữ liệu từ bảng "thuthap" trong MySQL
def process_data(engine, stop_event):
    while not stop_event.is_set():
        print("start")
        try:
            # Đọc giá trị last_processed_id_old từ bảng status (nếu có)
            with engine.connect() as conn:
                try:
                    # Thực hiện truy vấn lấy giá trị last_processed_id_old
                    result = conn.execute(text("SELECT last_processed_id_old FROM status1 WHERE id = 1"))
                    row = result.fetchone()

                    # Kiểm tra nếu dòng tồn tại và giá trị không NULL
                    if row and row[0] is not None:
                        last_processed_id_old = row[0]
                    else:
                        # Nếu không có giá trị, gán giá trị mặc định
                        last_processed_id_old = 0
                        print(
                            "Không tìm thấy giá trị hợp lệ trong cột last_processed_id_old. Sử dụng giá trị mặc định = 0.")

                    print(f"Last processed ID (old): {last_processed_id_old}")

                except Exception as e:
                    print(f"Lỗi khi truy vấn bảng status1: {e}")
                    last_processed_id_old = 0  # Gán giá trị mặc định nếu xảy ra lỗi

            # Lấy last_processed_id_new (giá trị ID lớn nhất hiện tại trong bảng thuthap)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT MAX(ID) FROM thuthap"))
                last_processed_id_new = result.scalar()  # Lấy giá trị ID lớn nhất
                print(f"Last processed ID (new): {last_processed_id_new}")

            # Kiểm tra nếu last_processed_id_old và last_processed_id_new bằng nhau
            if last_processed_id_old == last_processed_id_new:
                print("Không có dữ liệu mới. Tiếp tục vòng lặp.")
                time.sleep(5)  # Đợi một chút trước khi kiểm tra lại
                continue  # Quay lại vòng lặp mà không thực hiện bất kỳ xử lý nào

            # Xác định phạm vi ID cần truy vấn
            if last_processed_id_old > 10000 and last_processed_id_old != 0 :
                start_id = last_processed_id_old - 10000
            else:
                start_id = 0  # Nếu last_processed_id_old nhỏ hơn hoặc bằng 6000, bắt đầu từ ID 0

            print(f"Start ID là: {start_id}")  # In giá trị start_id khi bắt đầu
            print(f"Truy vấn từ ID: {start_id} đến ID: {last_processed_id_new}")  # In ra phạm vi truy vấn

            # Truy vấn dữ liệu từ bảng thuthap với phạm vi từ start_id đến last_processed_id_new
            query = text(
                f"SELECT * FROM thuthap WHERE ID > {start_id} AND ID <= {last_processed_id_new} ORDER BY ID ASC FOR UPDATE")
            print(f"Đang thực thi câu lệnh truy vấn: {query}")  # In ra câu lệnh SQL trước khi thực hiện
            data2 = pd.read_sql(query, con=engine)

            if data2.empty:
                print("Không có dữ liệu mới để xử lý.")
                time.sleep(1)
                continue

            # Cập nhật last_processed_id_old thành last_processed_id_new chỉ khi thành công
            last_processed_id_old = last_processed_id_new
            # Cập nhật last_processed_id_old trong bảng status
            update_query = text("UPDATE status1 SET last_processed_id_old = :last_processed_id_old WHERE id = 1")
            with engine.connect() as conn:
                    conn.execute(update_query, {'last_processed_id_old': last_processed_id_old})
                    conn.commit()  # Thêm dòng này nếu cần commit thay đổi
            print(f"Cập nhật thành công: last_processed_id (old) = {last_processed_id_old}")

            print(f"Dữ liệu mới từ thuthap:\n{data2.head()}")

            # Chuyển đổi cột 'Amplitude' thành dữ liệu kiểu số thực
            data2['Amplitude'] = pd.to_numeric(data2['Amplitude'], errors='coerce')
            data2 = data2.dropna(subset=['Amplitude'])
            signal = data2['Amplitude'].values

            # Kiểm tra dữ liệu trước khi tính toán
            if len(signal) == 0:
                print("Dữ liệu 'Amplitude' không hợp lệ, bỏ qua.")
                continue

            # Tính toán RMS với cửa sổ trượt
            window_size = 3
            kernel_size = 3
            rms_values = calculate_rms(signal, window_size)
            smoothed_rms = medfilt(rms_values, kernel_size=kernel_size)

            # Tìm đỉnh từ giá trị RMS
            min_distance = 5000
            peaks, _ = find_peaks(smoothed_rms, height=0.01, distance=min_distance)

            if len(peaks) > 1:
                print(f"Đã phát hiện {len(peaks)} đỉnh.")

                # Tính toán đặc trưng cho từng chu kỳ
                cycles = [signal[peaks[i]:peaks[i + 1]] for i in range(len(peaks) - 1)]
                cycle_features = []

                for cycle in cycles:
                    freqs, psd = welch(cycle)
                    cycle_features.append({
                        'length': len(cycle),
                        'psd_mean': np.mean(psd),
                        'kurtosis': stats.kurtosis(cycle),
                        'skewness': stats.skew(cycle),
                        'mean': np.mean(cycle),
                        'std_dev': np.std(cycle),
                        'num_peaks_above_threshold': len(find_peaks(cycle, height=0.005, distance=500)[0])
                    })

                df = pd.DataFrame(cycle_features)

                if df.empty:
                    print("Không có đặc trưng nào để lưu vào bảng 'xuly'.")
                    continue

                # In dữ liệu trước khi lưu vào bảng 'xuly'
                print(f"Dữ liệu đặc trưng chuẩn bị lưu vào bảng 'xuly':\n{df.head()}")

                # Lưu kết quả đặc trưng vào bảng xuly
                save_data(df, engine)


        except Exception as e:
            print(f"Lỗi trong quá trình xử lý dữ liệu: {e}")

        time.sleep(10)


def classify_data():
    model = load('modelAI1.pkl')
    print("Mô hình đã được nạp từ file 'modelAI1 .pkl'.")

    # Khởi tạo last_classified_id1 từ bảng status
    with engine.connect() as conn:
        result = conn.execute(text("SELECT last_classified_id1 FROM status WHERE id = 1")).fetchone()
        last_classified_id1 = result[0] if result else 0

    while not stop_event.is_set():
        try:
            query = f"SELECT * FROM xuly WHERE ID1 > {last_classified_id1}"
            data4 = pd.read_sql(query, con=engine)

            if not data4.empty:
                print("Đang phân loại dữ liệu từ bảng xuly...")

                # Kiểm tra các cột cần thiết
                required_features = ["length", "psd_mean", "kurtosis", "skewness","mean", "std_dev", "num_peaks_above_threshold"]
                if not all(feature in data4.columns for feature in required_features):
                    raise ValueError("Thiếu các cột cần thiết trong bảng xuly.")

                # Trích xuất đặc trưng từ dữ liệu
                x_new = data4[required_features]
                predictions = model.predict(x_new)

                # Tạo DataFrame kết quả phân loại
                output = pd.DataFrame({
                    'ID': data4['ID1'],
                    'pl1': predictions
                })
                # Lưu kết quả vào bảng 'phanloai'
                output.to_sql("phanloai", con=engine, if_exists="append", index=False)
                print("Kết quả phân loại đã được lưu vào bảng phanloai.")

                # Cập nhật last_classified_id1
                last_classified_id1 = data4['ID1'].max()
                update_classified_id_query = text("UPDATE status SET last_classified_id1 = :last_classified_id1 WHERE id = 1")
                with engine.connect() as conn:
                    conn.execute(update_classified_id_query, {"last_classified_id1": last_classified_id1})
            else:
                #print("Không có dữ liệu mới để phân loại.")
                continue
        except Exception as e:
            print(f"Lỗi khi phân loại dữ liệu: {e}")

        time.sleep(1)



# Bắt đầu các luồng và truyền các đối số vào hàm
record_thread = threading.Thread(target=record_data)
process_thread = threading.Thread(target=process_data, args=(engine, stop_event))  # Truyền engine và stop_event
classify_thread = threading.Thread(target=classify_data)

record_thread.start()
process_thread.start()
classify_thread.start()


# Nhấn phím Space để dừng các luồng
keyboard.wait('space')
stop_event.set()  # Kích hoạt sự kiện dừng

# Đợi tất cả các luồng kết thúc
record_thread.join()
process_thread.join()
classify_thread.join()

print("Chương trình đã kết thúc.")
