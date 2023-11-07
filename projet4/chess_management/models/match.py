from models.player import Player


class Match:
    """
    Represents a chess match between two players.
    """

    def __init__(self, player1: Player, player2: Player, score1: float = None, score2: float = None) -> None:
        """
        Initializes a Match instance.

        Args:
            player1 (Player): The first player in the match.
            player2 (Player): The second player in the match.
            score1 (float, optional): The score of the first player. None if not yet set.
            score2 (float, optional): The score of the second player. None if not yet set.
        """
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
        self.total_points_player1 = 0
        self.total_points_player2 = 0

    @property
    def is_finished(self) -> bool:
        """
        Checks if the match has ended.

        Returns:
            bool: True if the scores for both players are set, otherwise False.
        """
        return self.score1 is not None and self.score2 is not None

    def set_scores(self, score1: float, score2: float) -> None:
        """
        Sets the scores for the players.

        Args:
            score1 (float): Score for player1.
            score2 (float): Score for player2.
        """
        self.score1 = score1
        self.score2 = score2

    def __str__(self) -> str:
        """ 
        Returns the string representation of the match.

        Returns:
            str: A string displaying the match details.
        """
        return f"{self.player1.get_full_name()} vs {self.player2.get_full_name()} - Scores: {self.score1}-{self.score2}"

    def get_winner(self) -> Player:
        """
        Returns the winner of the match or None if it's a draw.

        Returns:
            Player or None: The winning player or None if the match ended in a draw.
        """
        if self.score1 is None or self.score2 is None:
            return None
        if self.score1 > self.score2:
            return self.player1
        elif self.score2 > self.score1:
            return self.player2
        return None

    def to_dict(self) -> dict:
        """
        Converts the match object to a dictionary.

        Returns:
            dict: A dictionary representation of the match.
        """
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2,
            "total_points_player1": self.total_points_player1,
            "total_points_player2": self.total_points_player2
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Match':
        """
        Creates a match instance from a dictionary representation.

        Args:
            data (dict): The dictionary containing match data.

        Returns:
            Match: A Match object created from the dictionary data.
        """
        player1 = Player.from_dict(data["player1"])
        player2 = Player.from_dict(data["player2"])

        # Assign the scores from the dictionary if they exist
        score1 = data.get("score1")
        score2 = data.get("score2")

        # Assign the total points from the dictionary if they exist
        total_points_player1 = data.get("total_points_player1", 0)  # Default to 0 if not present
        total_points_player2 = data.get("total_points_player2", 0)  # Default to 0 if not present

        match = cls(player1, player2, score1, score2)
        match.total_points_player1 = total_points_player1
        match.total_points_player2 = total_points_player2

        return match