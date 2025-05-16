import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import sys

sys.stdout.reconfigure(encoding='utf-8')
# Load your dataset features for prediction
df = pd.read_csv("features.csv", index_col=False)

# Extract and normalize features exactly as done during training
sk_features = df[['Kurtosis', 'Skewness']].values
psd_columns = [str(i) for i in range(1, 27)]
psd_features = df[psd_columns].values

# Combine features
X = np.hstack((psd_features, sk_features))

# Load the saved model
model = tf.keras.models.load_model("model.keras")

# Make predictions (probabilities)
pred_probs = model.predict(X)

# Convert probabilities to binary class (threshold 0.5)
pred_classes = (pred_probs > 0.5).astype(int)

print(pred_classes.flatten())
