import librosa
import numpy as np
import logging
from tensorflow.keras.models import load_model
from config import MODEL_PATH

class SirenDetectorCNN:
    def __init__(self):
        try:
            self.model = load_model(MODEL_PATH)
            logging.info("Modèle audio chargé.")
        except Exception as e:
            logging.error(f"Erreur lors du chargement du modèle audio : {e}")
            raise

    def extract_features(self, file):
        try:
            audio, sr = librosa.load(file, duration=3)
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
            return np.mean(mfcc.T, axis=0)
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction des features audio : {e}")
            raise

    def predict(self, file="audio.wav"):
        try:
            features = self.extract_features(file)
            features = features.reshape(1, -1)
            prediction = self.model.predict(features, verbose=0)
            return prediction[0][0] > 0.5
        except Exception as e:
            logging.error(f"Erreur lors de la prédiction audio : {e}")
            return False
