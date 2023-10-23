from datetime import datetime
from models.tournament import Tournament


class Round:
    def __init__(self, name: str, start_time: datetime = None, end_time: datetime = None, matches: list[tuple[list[str], list[float]]] = None):
        """
        Initialize a Round instance.

        :param name: The name or identifier of the round.
        :param start_time: The date and time when the round starts (default is None).
        :param end_time: The date and time when the round ends (default is None).
        :param matches: A list to store the matches for the round (default is an empty list).
        """
        self.name = name
        self.start_time = start_time  # Date and time when the round starts
        self.end_time = end_time  # Date and time when the round ends
        self.matches = matches or []  # A list to store the matches for the round

    def __str__(self) -> str:
        """
        Return a string representation of the Round instance.

        :return: A string describing the round, including its name, the number of matches, start time, and end time.
        """
        return f"Round {self.name} - Matches: {len(self.matches)} - Start Time: {self.start_time} - End Time: {self.end_time}"

    def generate_round_name(self, tournament: Tournament) -> str:
        """
        Generate the name of the round based on the round number of the parent tournament.

        :param tournament: The Tournament instance to which this round belongs.
        :return: The name of the round, e.g., "Round 1", "Round 2", etc.
        """
        round_number = tournament.round_number
        return f"Round {round_number}"

    def start_round(self):
        """
        Start the round and set the start time to the current date and time.
        """
        self.start_time = datetime.now()

    def end_round(self):
        """
        End the round and set the end time to the current date and time.
        """
        self.end_time = datetime.now()

    def add_match(self, players: list[str], scores: list[float]):
        """
        Add a match to the round.

        :param players: A list of two players participating in the match.
        :param scores: A list of two scores corresponding to the players.
        :raises ValueError: If the length of the players or scores lists is not exactly 2.
        """
        if len(players) != 2 or len(scores) != 2:
            raise ValueError("A match should have exactly 2 players and 2 scores.")
        match = (players, scores)
        self.matches.append(match)


