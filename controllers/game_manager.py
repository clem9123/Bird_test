import random
from controllers.data_manager import DataManager

class GameManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.oiseaux = self.data_manager.data

    def choisir_oiseau(self):
        return random.choice(self.oiseaux)

    def enregistrer_reponse(self, nom, correct):
        oiseau = self.data_manager.get_oiseau(nom)
        if oiseau:
            if correct:
                oiseau["nb_bonne_reponses"] += 1
            else:
                oiseau["nb_mauvaise_reponses"] += 1
            # Sauvegarder les données uniquement lorsque c'est nécessaire
            self.data_manager.save_data()
