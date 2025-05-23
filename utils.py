import json

def charger_dico_json(nom_fichier):
    import os
    if os.path.exists(nom_fichier):
        try:
            with open(nom_fichier, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    else:
        return {}
    
def enregistrer_bordure(dico_bordures, etat_id, bordure, grid_width):
    nb_actions = grid_width - 1  # Pour un carré 2x2
    dico_bordures[str(etat_id)] = {
        "bordure": bordure,
        "Q_table": [0.0 for _ in range(nb_actions)]
        }

def sauvegarder_dico_json(dico, nom_fichier):
    with open(nom_fichier, "w") as f:
        json.dump(dico, f, indent=4)

def matrice_deja_presente(dico, matrice):
    for v in dico.values():
        if v == matrice:
            return True
    return False