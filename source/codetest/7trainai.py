import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score
import os

# Disable TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    # Load data - disable index printing to avoid encoding issues
    df = pd.read_csv("features.csv", index_col=False)
    
    # Extract labels and features
    y = df['Label'].values
    sk_features = df[['Kurtosis', 'Skewness']].values
    psd_columns = [str(i) for i in range(1, 27)]
    psd_features = df[psd_columns].values
    
    # Normalize PSD and sk_features
    psd_features = StandardScaler().fit_transform(psd_features)
    sk_features = StandardScaler().fit_transform(sk_features)
    
    # Combine normalized PSD and sk_features
    X = np.hstack((psd_features, sk_features))
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Single layer neural network (1NN)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, activation='sigmoid', input_shape=(X.shape[1],))
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Minimal printing callback
    class MinimalPrintingCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            if epoch % 10 == 0:  # Print only every 10 epochs
                print(f"Epoch {epoch}: acc={logs['accuracy']:.4f}")
    
    # Train model
    model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=2,
        verbose=0,
        callbacks=[MinimalPrintingCallback()]
    )
    
    # Evaluate on test set
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    y_pred_test = (model.predict(X_test, verbose=0) > 0.5).astype(int)
    test_precision = precision_score(y_test, y_pred_test)
    
    # Predict on full dataset
    y_pred_full = (model.predict(X, verbose=0) > 0.5).astype(int)
    full_acc = np.mean(y_pred_full.flatten() == y)
    full_precision = precision_score(y, y_pred_full.flatten())
    
    # Save predictions
    results_df = pd.DataFrame({
        'Actual': y,
        'Predicted': y_pred_full.flatten()
    })
    results_df.to_csv('full_predictions.csv', index=False)
    
    # Save metrics
    with open("results.txt", "w") as f:
        f.write(f"Test Accuracy: {test_acc:.4f}\n")
        f.write(f"Test Precision: {test_precision:.4f}\n")
        f.write(f"\nFull Dataset Results:\n")
        f.write(f"Full Dataset Accuracy: {full_acc:.4f}\n")
        f.write(f"Full Dataset Precision: {full_precision:.4f}\n")
    
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Precision: {test_precision:.4f}")
    print(f"\nFull Dataset Results:")
    print(f"Full Dataset Accuracy: {full_acc:.4f}")
    print(f"Full Dataset Precision: {full_precision:.4f}")
    
    # Save model
    model.save("test.keras")

except Exception as e:
    # Write error to file instead of printing
    with open("error_log.txt", "w") as f:
        f.write(f"Error: {str(e)}")
    print("Error occurred. See error_log.txt for details.")
