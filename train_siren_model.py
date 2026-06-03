import numpy as np
import librosa
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

DATASET_PATH = "dataset/"

def extract(file):
    audio, sr = librosa.load(file, duration=3)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

X, y = [], []

for label, folder in enumerate(["no_siren", "siren"]):
    path = os.path.join(DATASET_PATH, folder)
    if not os.path.exists(path):
        continue
    for file in os.listdir(path):
        feat = extract(os.path.join(path, file))
        X.append(feat)
        y.append(label)

X = np.array(X)
y = np.array(y)

# Split en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Dense(128, activation='relu', input_shape=(40,)),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, validation_split=0.2)

# Évaluation
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.2f}")

y_pred = (model.predict(X_test) > 0.5).astype(int)
print(classification_report(y_test, y_pred))

os.makedirs("models", exist_ok=True)
model.save("models/siren_model.h5")
