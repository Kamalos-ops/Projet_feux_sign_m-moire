from ultralytics import YOLO
import cv2
import logging
from config import YOLO_MODEL, CAMERA_SOURCES

class MultiCameraYOLO:
    def __init__(self):
        try:
            self.model = YOLO(YOLO_MODEL)
            self.caps = []
            for src in CAMERA_SOURCES:
                cap = cv2.VideoCapture(src)
                if not cap.isOpened():
                    logging.warning(f"Caméra {src} non disponible.")
                    self.caps.append(None)
                else:
                    self.caps.append(cap)
            logging.info("YOLO initialisé.")
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation YOLO : {e}")
            raise

    def get_counts(self):
        counts = []
        for i, cap in enumerate(self.caps):
            if cap is None:
                counts.append(0)
                continue
            try:
                ret, frame = cap.read()
                if not ret:
                    logging.warning(f"Impossible de lire la caméra {i}.")
                    counts.append(0)
                    continue
                results = self.model(frame)
                count = 0
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        if cls in [2, 3, 5, 7]:  # voiture, moto, bus, camion
                            count += 1
                counts.append(count)
            except Exception as e:
                logging.error(f"Erreur lors du traitement de la caméra {i} : {e}")
                counts.append(0)
        return counts
