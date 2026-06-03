class DecisionSystem:
    def __init__(self):
        self.last_lane = -1
        self.cycle_count = 0

    def decide(self, counts, siren_detected):
        if siren_detected:
            # Priorité aux sirènes : choisir la voie avec le plus de véhicules
            lane = counts.index(max(counts))
            return "PRIORITY", lane

        # Mode normal : logique améliorée
        # Si aucune voie n'a de véhicules, rester sur la dernière
        if all(c == 0 for c in counts):
            return "NORMAL", self.last_lane if self.last_lane != -1 else 0

        # Trouver la voie avec le plus de véhicules
        max_count = max(counts)
        candidates = [i for i, c in enumerate(counts) if c == max_count]

        # Si plusieurs voies ont le même nombre, alterner ou choisir la suivante
        if len(candidates) > 1:
            # Éviter de rester sur la même voie trop longtemps
            self.cycle_count += 1
            if self.cycle_count % 3 == 0:  # Alterner tous les 3 cycles
                lane = (self.last_lane + 1) % len(counts)
            else:
                lane = candidates[0]  # Prendre la première
        else:
            lane = candidates[0]

        self.last_lane = lane
        return "NORMAL", lane
