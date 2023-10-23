class Player:
    def __init__(self, chess_id, first_name, last_name, birthdate, total_points=0.0):
        self.chess_id = chess_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.total_points = total_points

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Chess ID: {self.chess_id}, Birthdate: {self.birthdate}, Total Points: {self.total_points})"

    def add_points(self, points):
        """
        Ajoute des points au total de points du joueur.

        :param points: Le nombre de points à ajouter.
        """
        self.total_points += points

    def get_full_name(self):
        """
        Renvoie le nom complet du joueur (par exemple, "John Doe").

        :return: Le nom complet du joueur.
        """
        return f"{self.first_name} {self.last_name}"