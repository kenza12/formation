import random
from models.player import Player
from models.match import Match
from models.round import Round


class Tournament:
    """
    Represents a chess tournament with multiple rounds and players.

    Attributes:
        name (str): Name of the tournament.
        location (str): Location where the tournament is held.
        start_date (str): Start date of the tournament.
        end_date (str): End date of the tournament.
        description (str): Description of the tournament.
        round_number (int): Total number of rounds in the tournament.
        current_round (int): The current round number.
        rounds (List[Round]): List of round objects.
        players (List[Player]): List of player objects.
        player_scores (Dict[str, float]): Dictionary mapping player chess IDs to their scores.
    """

    def __init__(self, name: str, location: str, start_date: str, end_date: str, description: str = "", round_number: int = 4) -> None:
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.round_number = round_number
        self.current_round = 1
        self.rounds = []
        self.players = []
        self.player_scores = {}

    def add_player(self, player: Player) -> None:
        """Add a new player to the tournament and initialize the score to 0"""
        self.players.append(player)
        self.player_scores[player.chess_id] = 0

    def add_points(self, player: Player, points: float) -> None:
        """Add points to a player's score."""
        self.player_scores[player.chess_id] += points

    def get_player_points(self, player: Player) -> float:
        """Retrieve the points of a player."""
        return self.player_scores.get(player.chess_id, 0)

    def start_new_round(self) -> None:
        """Start a new round in the tournament."""

        # Players are shuffled in the first round and sorted by score for subsequent rounds.
        if self.current_round == 1:
            self.shuffle_players()
        else:
            self.players.sort(key=self.player_sort_key, reverse=True)

        # If no new matches can be formed or the maximum number of rounds is reached, the tournament ends.
        if self.is_ended():
            print("No new matches can be formed. The tournament has ended.")
            return

        # Generates player pairs for the current round. It avoids forming pairs that have already played together in previous rounds.
        new_round, _ = self.generate_round_pairs()
        self.rounds.append(new_round)

        # Marks the start time of the round.
        new_round.start_round()

        print(f"Round {self.current_round} of the tournament has started.")
        self.current_round += 1

    def generate_round_pairs(self) -> tuple:
        """This method pairs players for the current round ensuring that no player is paired together more than once and that two players who have already played together in a previous match are not paired together again."""
        
        # Fetch previously played matches
        played_matches = {(match.player1.chess_id, match.player2.chess_id) for r in self.rounds for match in r.matches}

        paired_players = set()
        current_round_matches = []
        current_round = Round(f"Round {self.current_round}")

        # Pair up players
        for i, player1 in enumerate(self.players):
            if player1.chess_id in paired_players:
                continue
            for j, player2 in enumerate(self.players[i+1:], start=i+1):
                if (player2.chess_id in paired_players) or \
                   ((player1.chess_id, player2.chess_id) in played_matches) or \
                   ((player2.chess_id, player1.chess_id) in played_matches):
                    continue

                current_round_matches.append((player1, player2))
                paired_players.update([player1.chess_id, player2.chess_id])
                break

        # Add matches to the current round
        for player1, player2 in current_round_matches:
            current_round.add_match(Match(player1, player2))

        return current_round, current_round_matches

    def shuffle_players(self) -> None:
        """Randomly shuffle the players."""
        random.shuffle(self.players)

    def player_sort_key(self, player: Player) -> tuple:
        """Sort key function for ordering players based on scores and IDs."""
        score = -self.player_scores.get(player.chess_id, 0)
        id = player.chess_id
        return (score, id)

    def is_ended(self) -> bool:
        """Check if the tournament has ended."""
        if len(self.rounds) >= self.round_number:
            return True
        _, pairs = self.generate_round_pairs()
        return len(pairs) == 0

    def __str__(self) -> str:
        """String representation of the tournament."""
        return f"Tournament: {self.name}, Location: {self.location}, Start Date: {self.start_date}, End Date: {self.end_date}, Current Round: {self.current_round}, Max Rounds: {self.round_number}, Description: {self.description}"

    def to_dict(self) -> dict:
        """Converts the tournament object to a dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "round_number": self.round_number,
            "current_round": self.current_round,
            "players": [player.to_dict() for player in self.players],
            "rounds": [round.to_dict() for round in self.rounds],
            "player_scores": self.player_scores
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Generates a Tournament instance from a dictionary representation."""
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data.get("description", ""),
            data.get("round_number", 4)
        )

        for player_data in data.get("players", []):
            tournament.add_player(Player.from_dict(player_data))

        for round_data in data.get("rounds", []):
            round = Round.from_dict(round_data)
            tournament.rounds.append(round)

        tournament.player_scores = data.get("player_scores", {})
        tournament.current_round = data.get("current_round", 1)

        return tournament

    def is_valid_player_count(self) -> bool:
        """Checks if the number of players is even."""
        return len(self.players) % 2 == 0

    def has_duplicate_players(self) -> bool:
        """Checks for the presence of duplicate players in the tournament."""
        ids = [player.chess_id for player in self.players]
        return len(ids) != len(set(ids))
