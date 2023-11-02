class Player:
    """
    Represents a chess player with relevant details.
    """
    
    def __init__(self, chess_id: int, first_name: str, last_name: str, birthdate: str) -> None:
        """
        Initializes a Player instance.

        Args:
            chess_id (int): Unique identification number for the player.
            first_name (str): The first name of the player.
            last_name (str): The last name of the player.
            birthdate (str): The birthdate of the player.
        """
        self.chess_id = chess_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate

    def __str__(self) -> str:
        """ 
        Returns the string representation of the player.

        Returns:
            str: A string displaying the player's full details.
        """
        return f"{self.last_name} {self.first_name} (Chess ID: {self.chess_id}, Birthdate: {self.birthdate})"

    def get_full_name(self) -> str:
        """
        Returns the full name of the player.

        Returns:
            str: The full name, consisting of the first name and last name.
        """
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        """
        Converts the player object to a dictionary.

        Returns:
            dict: A dictionary representation of the player.
        """
        return {
            "chess_id": self.chess_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
        }

    @classmethod
    def from_dict(cls, player_data: dict) -> 'Player':
        """
        Creates a player instance from a dictionary representation.

        Args:
            player_data (dict): The dictionary containing player data.

        Returns:
            Player: A Player object created from the dictionary data.
        """
        return cls(
            player_data["chess_id"],
            player_data["first_name"],
            player_data["last_name"],
            player_data["birthdate"]
        )