import serial
import logging
from config import SERIAL_PORT, BAUD_RATE

class ArduinoComm:
    def __init__(self):
        try:
            self.arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            logging.info("Connexion Arduino établie.")
        except Exception as e:
            logging.error(f"Erreur lors de la connexion à Arduino : {e}")
            raise

    def send_lane(self, lane):
        try:
            self.arduino.write((f"LANE_{lane}\n").encode())
            logging.debug(f"Commande envoyée : LANE_{lane}")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi à Arduino : {e}")
