import json

def get_recommendations(skin_type: str):
    with open("backend/data/recommendations.json") as f:
        rules = json.load(f)

    # Retourne une liste vide si la clé n'existe pas
    return rules.get(skin_type, [])
