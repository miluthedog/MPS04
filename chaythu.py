import random
import threading
import time

import keyboard
import numpy as np
import pandas as pd
import scipy.stats as stats
from joblib import load
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

stop_event = threading.Event()


# Hàm ghi dữ liệu từ cảm biến và lưu vào MySQL

def generate_random_data(duration_seconds=50):
    # Số mẫu (kích thước dãy dữ liệu) = duration * tần suất mẫu (target_sample_rate)
    target_sample_rate = 441  # Thay đổi tần suất mẫu nếu cần
    num_samples = duration_seconds * target_sample_rate

    # Tạo dãy các giá trị float ngẫu nhiên
    random_data = [random.uniform(-0.0136108, 0.01502637) for _ in range(num_samples)]

    return random_data

# Hàm ghi dữ liệu ngẫu nhiên vào MySQL
def record_data():
    print("Bắt đầu tạo và lưu dữ liệu ngẫu nhiên trong 50 giây...")

    # Tạo dãy giá trị ngẫu nhiên trong khoảng 50 giây
    random_data = generate_random_data(duration_seconds=500)

    # Tạo DataFrame với Amplitude
    df = pd.DataFrame({
        "Amplitude": random_data,
    })

    # Lưu DataFrame vào MySQL
    df.to_sql("thuthap", con=engine, if_exists="append", index=False)
    df.to_sql("cbgt", con=engine, if_exists="append", index=False)
    print("Dữ liệu đã được lưu vào bảng 'thuthap' trong MySQL.")


# Đọc dữ liệu từ bảng "thuthap" trong MySQL
def process_data():
    last_processed_id = 0
    while not stop_event.is_set():
        try:
            # Truy vấn dữ liệu từ bảng thuthap
            query = f"SELECT * FROM thuthap WHERE ID > {last_processed_id}"
            print(f"Truy vấn: {query}")
            data2 = pd.read_sql(query, con=engine)

            if data2.empty:
                print("Không có dữ liệu mới để xử lý.")
                time.sleep(5)
                continue

            print(f"Dữ liệu mới từ thuthap:\n{data2.head()}")

            # Chuyển đổi cột 'Amplitude' thành dữ liệu kiểu số thực
            data2['Amplitude'] = pd.to_numeric(data2['Amplitude'], errors='coerce')
            data2 = data2.dropna(subset=['Amplitude'])
            signal = data2['Amplitude'].values

            # Tính toán RMS với cửa sổ trượt
            window_size = 5
            rms_values = [np.sqrt(np.mean(signal[i:i + window_size] ** 2)) for i in range(len(signal) - window_size + 1)]
            rms_values = np.array(rms_values)
            filtered_rms = medfilt(rms_values, kernel_size=5)


            # Tìm đỉnh từ giá trị RMS
            min_distance = 7700
            peaks, _ = find_peaks(filtered_rms, height=0.01, distance=min_distance)

            if len(peaks) >= 2:
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

                # Lưu kết quả đặc trưng vào bảng xuly sau khi loại bỏ trùng lặp
                save_unique_data(df, engine)

                # Cập nhật last_processed_id chỉ khi thành công
                last_processed_id = data2['ID'].max()

                # Cập nhật last_processed_id trong bảng status
                update_query = text("UPDATE status SET last_processed_id = :last_processed_id WHERE id = 1")
                with engine.connect() as conn:
                    conn.execute(update_query, {'last_processed_id': last_processed_id})
                print(f"Cập nhật thành công: last_processed_id = {last_processed_id}")

        except Exception as e:
            print(f"Lỗi trong quá trình xử lý dữ liệu: {e}")

        time.sleep(5)

def save_unique_data(df, engine):
    """
    Lưu dữ liệu từ DataFrame vào bảng 'xuly', đảm bảo không lưu các dòng trùng lặp.
    """
    # Truy vấn dữ liệu hiện có từ bảng 'xuly'
    try:
        existing_data = pd.read_sql("SELECT * FROM xuly", con=engine)
    except Exception as e:
        print(f"Lỗi khi truy vấn bảng 'xuly': {e}")
        existing_data = pd.DataFrame()  # Nếu xảy ra lỗi, giả sử bảng xuly đang trống

    # Loại bỏ các bản ghi trùng lặp
    unique_data = df.merge(existing_data,
                           on=['length', 'psd_mean', 'kurtosis', 'skewness', 'mean', 'std_dev',
                               'num_peaks_above_threshold'],
                           how='left', indicator=True)
    new_data = unique_data[unique_data['_merge'] == 'left_only']
    new_data = new_data.drop(columns=['_merge'])

    # Lưu các bản ghi mới vào bảng 'xuly'
    if not new_data.empty:
        try:
            new_data.to_sql("xuly", con=engine, if_exists="append", index=False)
            print(f"Đã lưu {len(new_data)} bản ghi mới vào bảng 'xuly'.")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào bảng 'xuly': {e}")
    else:
        print("Không có bản ghi mới để lưu vào bảng 'xuly'.")


def classify_data():
    model = load('model.pkl')
    print("Mô hình đã được nạp từ file 'model.pkl'.")

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
                required_features = ["length", "psd_mean", "kurtosis", "skewness", "mean", "std_dev", "num_peaks_above_threshold"]
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
                print("Không có dữ liệu mới để phân loại.")

        except Exception as e:
            print(f"Lỗi khi phân loại dữ liệu: {e}")

        time.sleep(10)



# Bắt đầu các luồng
record_thread = threading.Thread(target=record_data)
process_thread = threading.Thread(target=process_data)
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


