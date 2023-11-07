from datetime import datetime
from models.match import Match


class Round:
    """Represents a round in a tournament with multiple matches.

    Attributes:
        name (str): Name of the round.
        start_time (datetime): Timestamp indicating when the round starts.
        end_time (datetime or None): Timestamp indicating when the round ends. None if the round hasn't ended yet.
        matches (list[Match]): List of matches in this round.
    """

    def __init__(self, name: str) -> None:
        """Initializes a Round instance.

        Args:
            name (str): Name of the round.
        """
        self.name = name
        # Set the start time to the current time
        self.start_time = None
        self.end_time = None
        self.matches = []

    def __str__(self) -> str:
        """Returns the string representation of the round.

        Returns:
            str: String displaying the round's details.
        """
        start_time_str = self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "N/A"
        end_time_str = self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "N/A"
        return f"Round {self.name} - Matches: {len(self.matches)} - Start Time: {start_time_str} - End Time: {end_time_str}"

    @property
    def is_finished(self) -> bool:
        """Checks if all matches in the round have ended.

        Returns:
            bool: True if all matches have ended, False otherwise.
        """
        return all(match.is_finished for match in self.matches)

    def start_round(self) -> None:
        """Marks the start time of the round."""
        # Update the start time to the current time
        self.start_time = datetime.now()

    def end_round(self) -> None:
        """Marks the end time of the round."""
        # Update the end time to the current time
        self.end_time = datetime.now()

    def add_match(self, match: Match) -> None:
        """Adds a match to the round.

        Args:
            match (Match): The match to be added.
        """
        self.matches.append(match)

    def to_dict(self) -> dict:
        """Converts the round object to a dictionary.

        Returns:
            dict: A dictionary representation of the round.
        """
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "is_finished": self.is_finished,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        """Creates a round instance from a dictionary representation.

        Args:
            data (dict): The dictionary containing round data.

        Returns:
            Round: A Round object created from the dictionary data.
        """
        round_instance = cls(data["name"])
        for match_data in data.get("matches", []):
            match = Match.from_dict(match_data)
            round_instance.matches.append(match)
        return round_instance
