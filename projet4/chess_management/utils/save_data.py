import os
import json


def save_tournament(tournament):
    """Sauvegarde le tournoi dans l'état dans le dossier data/tournaments au format JSON.

    Args:
        tournament (Object): Tournoi du jeu d'échecs

    Returns:
        file_path (str) : chemin du fichier du tournoi JSON
        dans le répertoire data/tournaments
    """
    if tournament:
        sanitized_name = tournament.name.replace(" ", "_")
        file_name = f"{sanitized_name}.json"
        directory = "data/tournaments"

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tournament.to_dict(), f, ensure_ascii=False, indent=4)

        return file_path
