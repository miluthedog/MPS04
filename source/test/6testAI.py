import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import sys

# Set correct output encoding for UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load data
data = pd.read_csv("features.csv")
X_vector = data.iloc[:, 3:].values  # PSD vector
X_ks = data.iloc[:, 1:3].values     # kurtosis, skew
y = data.iloc[:, 0].values          # label

# Split into train/test
Xv_train, Xv_test, Xks_train, Xks_test, y_train, y_test = train_test_split(
    X_vector, X_ks, y, test_size=0.2, random_state=42)

# Build model
input_vector = tf.keras.layers.Input(shape=(52,))
input_ks = tf.keras.layers.Input(shape=(2,))

x = tf.keras.layers.Dense(32, activation='relu')(input_vector)
combined = tf.keras.layers.Concatenate()([x, input_ks])
out = tf.keras.layers.Dense(1, activation='sigmoid')(combined)

model = tf.keras.Model(inputs=[input_vector, input_ks], outputs=out)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit([Xv_train, Xks_train], y_train, epochs=100, batch_size=32, validation_data=([Xv_test, Xks_test], y_test))

# Evaluate the model
loss, acc = model.evaluate([Xv_test, Xks_test], y_test)
print(f"Test Accuracy: {acc:.4f}")

# Batch test: Predict 10 random samples
batch_size = 10
indices = np.random.randint(0, len(Xv_test), batch_size)  # Random indices from the test set
sample_vectors = Xv_test[indices]
sample_ks = Xks_test[indices]
true_labels = y_test[indices]

# Predict in batch
preds = model.predict([sample_vectors, sample_ks])

# Print the results for each sample in the batch
for i in range(batch_size):
    true_label = true_labels[i]
    pred_score = preds[i, 0]
    pred_label = int(pred_score > 0.5)  # Convert score to label (0 or 1)
    print(f"True Label: {true_label}, Predicted Score: {pred_score:.4f} -> Predicted Label: {pred_label}")
