import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Đọc dữ liệu từ file CSV
file_path = "C:/Users/User/Desktop/trainingAI/loi1.csv"
data = pd.read_csv(file_path)

# Kiểm tra dữ liệu
print(data.head())

# Tách dữ liệu thành đặc trưng (features) và nhãn (label)
X = data[["length", "psd_mean", "kurtosis", "skewness", "mean", "std_dev", "num_peaks_above_threshold"]]
y = data["pl"]

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình (ví dụ dùng RandomForest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Lưu mô hình vào file modelAI.pkl
try:
    dump(model, 'modelAI1.pkl')  # Lưu mô hình với joblib
    print("Mô hình đã được lưu vào file 'modelAI1.pkl'.")
except Exception as e:
    print(f"Lỗi khi lưu mô hình: {e}")
