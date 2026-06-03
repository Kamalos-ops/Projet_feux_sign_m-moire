import time
import logging
from yolo_detector import MultiCameraYOLO
from audio_cnn import SirenDetectorCNN
from decision import DecisionSystem
from arduino_comm import ArduinoComm

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        yolo = MultiCameraYOLO()
        audio = SirenDetectorCNN()
        decision = DecisionSystem()
        arduino = ArduinoComm()
        logging.info("Système initialisé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de l'initialisation : {e}")
        return

    while True:
        try:
            counts = yolo.get_counts()
            siren = audio.predict()

            mode, lane = decision.decide(counts, siren)

            logging.info(f"Counts: {counts}, Siren: {siren}, Mode: {mode}, Lane: {lane}")

            arduino.send_lane(lane)
            time.sleep(2)
        except Exception as e:
            logging.error(f"Erreur dans la boucle principale : {e}")
            time.sleep(5)  # Attendre avant de réessayer

if __name__ == "__main__":
    main()
