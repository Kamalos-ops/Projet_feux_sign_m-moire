import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(__file__))

from decision import DecisionSystem
from audio_cnn import SirenDetectorCNN
from yolo_detector import MultiCameraYOLO
from arduino_comm import ArduinoComm

class TestDecisionSystem(unittest.TestCase):
    def setUp(self):
        self.decision = DecisionSystem()

    def test_decide_priority(self):
        counts = [1, 5, 2, 3]
        siren = True
        mode, lane = self.decision.decide(counts, siren)
        self.assertEqual(mode, "PRIORITY")
        self.assertEqual(lane, 1)  # Voie avec max véhicules

    def test_decide_normal(self):
        counts = [1, 5, 2, 3]
        siren = False
        mode, lane = self.decision.decide(counts, siren)
        self.assertEqual(mode, "NORMAL")
        self.assertEqual(lane, 1)

    def test_decide_no_vehicles(self):
        counts = [0, 0, 0, 0]
        siren = False
        mode, lane = self.decision.decide(counts, siren)
        self.assertEqual(mode, "NORMAL")
        self.assertEqual(lane, 0)  # Défaut

class TestSirenDetectorCNN(unittest.TestCase):
    @patch('audio_cnn.load_model')
    def setUp(self, mock_load):
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        self.audio = SirenDetectorCNN()

    @patch('audio_cnn.librosa.load')
    @patch('audio_cnn.librosa.feature.mfcc')
    def test_predict_siren(self, mock_mfcc, mock_load):
        mock_load.return_value = (MagicMock(), 22050)
        mock_mfcc.return_value = MagicMock()
        mock_mfcc.return_value.T = [[1]*40]
        self.audio.model.predict.return_value = [[0.8]]
        result = self.audio.predict()
        self.assertTrue(result)

    @patch('audio_cnn.librosa.load')
    @patch('audio_cnn.librosa.feature.mfcc')
    def test_predict_no_siren(self, mock_mfcc, mock_load):
        mock_load.return_value = (MagicMock(), 22050)
        mock_mfcc.return_value = MagicMock()
        mock_mfcc.return_value.T = [[1]*40]
        self.audio.model.predict.return_value = [[0.3]]
        result = self.audio.predict()
        self.assertFalse(result)

class TestMultiCameraYOLO(unittest.TestCase):
    @patch('yolo_detector.YOLO')
    @patch('yolo_detector.cv2.VideoCapture')
    def setUp(self, mock_cap, mock_yolo):
        mock_cap.return_value.isOpened.return_value = True
        self.yolo = MultiCameraYOLO()

    def test_get_counts(self):
        # Mock frame et results
        mock_frame = MagicMock()
        self.yolo.caps[0].read.return_value = (True, mock_frame)
        mock_results = MagicMock()
        mock_box = MagicMock()
        mock_box.cls = [2]  # Voiture
        mock_results.boxes = [mock_box]
        self.yolo.model.return_value = [mock_results]
        counts = self.yolo.get_counts()
        self.assertEqual(len(counts), 4)
        self.assertGreaterEqual(counts[0], 0)

class TestArduinoComm(unittest.TestCase):
    @patch('arduino_comm.serial.Serial')
    def setUp(self, mock_serial):
        self.arduino = ArduinoComm()

    def test_send_lane(self):
        self.arduino.send_lane(1)
        self.arduino.arduino.write.assert_called_with(b"LANE_1\n")

if __name__ == '__main__':
    unittest.main()