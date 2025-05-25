import json



def charger_dico_json(nom_fichier):
    """
    Charge un dictionnaire à partir d'un fichier JSON.
    """
    import os
    if os.path.exists(nom_fichier):
        try:
            with open(nom_fichier, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    else:
        return {}
    

def sauvegarder_dico_json(dico, nom_fichier):
    """
    Sauvegarde un dictionnaire dans un fichier JSON.
    """
    with open(nom_fichier, "w") as f:
        json.dump(dico, f, indent=4)
