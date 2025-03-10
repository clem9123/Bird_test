import json

class DataManager:
    def __init__(self, filepath="data/birds.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get_oiseau(self, nom):
        for oiseau in self.data:
            if oiseau["nom_vernaculaire"] == nom:
                return oiseau
        return None


