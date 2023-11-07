import json
import os
from models.tournament import Tournament


def load_state(file_name):
    """Cette méthode va charger un fichier JSON du tournoi.

    Args:
        file_name (file): le fichier JSON contenant les informations du
        tournoi dans l'état

    Returns:
        Tournament (Object): Tournoi chargé
    """
    file_path = os.path.join("data/tournaments", file_name)

    try:
        # Chargez les données depuis le fichier JSON spécifié
        with open(file_path, "r") as file:
            tournament_data = json.load(file)

        # Créez un nouvel objet Tournament en utilisant from_dict
        tournament = Tournament.from_dict(tournament_data)
        print("Données chargées avec succès.")
        return tournament
    except FileNotFoundError:
        print("Le fichier de données n'existe pas. Utilisez 'Sauvegarder le tournoi' pour enregistrer l'état actuel.")
        return None
