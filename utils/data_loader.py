import json
import os

# Define the path to your JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/birds.json")

def charger_donnees(filepath=DATA_FILE):
    """Load bird data from the JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"oiseaux": []}  # Return an empty structure if the file is missing or corrupted

def sauvegarder_donnees(donnees, fichier=DATA_FILE):
    """Save bird data to the JSON file."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
