#!/usr/bin/env python3
"""
Script de test d'intégration pour simuler une exécution courte du système.
Utilise des mocks pour éviter les dépendances matérielles.
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire au path
sys.path.insert(0, os.path.dirname(__file__))

def test_integration():
    print("Test d'intégration : Simulation d'une boucle principale...")

    # Mock les composants dans leurs modules respectifs
    with patch('yolo_detector.YOLO') as mock_yolo, \
         patch('yolo_detector.cv2.VideoCapture') as mock_cap, \
         patch('audio_cnn.load_model') as mock_load, \
         patch('arduino_comm.serial.Serial') as mock_serial, \
         patch('audio_cnn.librosa.load') as mock_librosa_load, \
         patch('audio_cnn.librosa.feature.mfcc') as mock_mfcc:

        # Configurer les mocks
        mock_cap.return_value.isOpened.return_value = True
        mock_cap.return_value.read.return_value = (True, MagicMock())
        mock_yolo.return_value = MagicMock()
        mock_load.return_value = MagicMock()
        mock_serial.return_value = MagicMock()
        mock_librosa_load.return_value = (MagicMock(), 22050)
        mock_mfcc.return_value = MagicMock()
        mock_mfcc.return_value.T = [[1]*40]

        # Mock les prédictions
        mock_model = mock_load.return_value
        mock_model.predict.return_value = [[0.8]]  # Sirène détectée

        mock_yolo_instance = mock_yolo.return_value
        mock_results = MagicMock()
        mock_box = MagicMock()
        mock_box.cls = [2]
        mock_results.boxes = [mock_box]
        mock_yolo_instance.return_value = [mock_results]

        try:
            # Importer et tester les composants
            from yolo_detector import MultiCameraYOLO
            from audio_cnn import SirenDetectorCNN
            from decision import DecisionSystem
            from arduino_comm import ArduinoComm

            yolo = MultiCameraYOLO()
            audio = SirenDetectorCNN()
            decision = DecisionSystem()
            arduino = ArduinoComm()

            counts = yolo.get_counts()
            siren = audio.predict()
            mode, lane = decision.decide(counts, siren)
            arduino.send_lane(lane)

            print(f"Simulation réussie : Counts={counts}, Siren={siren}, Mode={mode}, Lane={lane}")
            return True

        except Exception as e:
            print(f"Erreur lors du test d'intégration : {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)