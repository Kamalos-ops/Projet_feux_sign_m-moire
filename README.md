# Système de Feux de Signalisation Intelligent

Ce projet implémente un système de gestion de feux de signalisation utilisant l'IA pour la détection de véhicules et de sirènes.

## Fonctionnalités
- Détection de véhicules en temps réel avec YOLO
- Détection de sirènes via CNN audio
- Logique de décision pour la priorité aux urgences
- Communication avec Arduino pour contrôler les feux

## Installation
1. Installer les dépendances : `pip install -r requirements.txt`
2. Entraîner le modèle audio : `python train_siren_model.py`
3. Lancer le système : `python main.py`

## Configuration
Modifier `config.py` pour adapter les paramètres (caméras, port série, etc.).

## Tests
- **Tests Unitaires** : `python -m pytest tests.py -v` (vérifie chaque module individuellement)
- **Test d'Intégration** : `python main.py` (avec matériel simulé ou réel)
- **Logs** : Consulter les messages de log pour le débogage

## Structure
- `main.py` : Point d'entrée principal
- `yolo_detector.py` : Détection de véhicules
- `audio_cnn.py` : Détection de sirènes
- `decision.py` : Logique de décision
- `arduino_comm.py` : Communication série
- `arduino_code/` : Code Arduino
- `tests.py` : Tests unitaires

## Améliorations Récentes
- Gestion d'erreurs et logging
- Logique de décision améliorée avec alternance
- Métriques d'évaluation pour le modèle audio
- Tests unitaires pour validation</content>
<parameter name="filePath">c:\Dev\Poo_3\Projet_feux_sign_mémoire\README.md