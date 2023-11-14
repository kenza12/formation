import random
from models.player import Player
from models.match import Match
from models.round import Round


class Tournament:
    """Represents a chess tournament with multiple rounds and players.

    The tournament is composed of a list of players and rounds, where each round
    contains a set of matches. The tournament tracks the current round and has
    a total number of rounds to be played.

    Attributes:
    # Tournament's identifying details
        name (str): Name of the tournament.
        location (str): Physical location where the tournament takes place.
        start_date (str): Start date of the tournament.
        end_date (str): End date of the tournament.
        description (str): Additional description of the tournament.

    # Structure of the tournament
        round_number (int): Total number of rounds in the tournament.
        current_round (int): The round that is currently being played.
        rounds (List[Round]): A list to store the rounds of the tournament.
        players (List[Player]): A list to store the players participating in the tournament.
    """

    def __init__(
        self,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        **kwargs
    ) -> None:
        """Initialize the Tournament with all necessary details."""
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = kwargs.get('description', "")
        self.round_number = kwargs.get('round_number', 4)
        self.current_round = 1
        self.rounds = []
        self.players = []

    def add_player(self, player: Player) -> None:
        """Adds a new player to the tournament's player list."""
        self.players.append(player)

    def get_player_points(self, player: Player) -> float:
        """Calculates the total points of a player by summing up the points from all matches."""
        total_points = 0
        for round in self.rounds:
            for match in round.matches:
                # Accumulate points if the player was part of the match
                if match.player1 == player:
                    total_points += match.score1
                elif match.player2 == player:
                    total_points += match.score2
        return total_points

    def start_new_round(self):
        """Begins a new round if the previous one has finished, otherwise alerts that the current round is still
        active."""
        if self.rounds and not self.rounds[-1].is_finished:
            print("The current round is not yet finished.")
            return

        # Shuffle players at the start or sort them by points for subsequent rounds.
        if self.current_round == 1:
            self.shuffle_players()
        else:
            self.players.sort(key=lambda player: -self.get_player_points(player))

        # Check if the tournament is finished before starting a new round.
        if self.is_ended():
            print("No new matches can be formed. The tournament has ended.")
            return

        # Generate player pairs for the new round
        new_round, _ = self.generate_round_pairs()
        self.rounds.append(new_round)
        new_round.start_round()
        print(f"Round {self.current_round} of the tournament has started.")
        self.current_round += 1

    def generate_round_pairs(self) -> tuple:
        """Generates unique player pairs for matches in the current round to ensure each player only plays against
        another once."""

        # Collect all previously played matches to avoid repeats.
        played_matches = {(match.player1.chess_id, match.player2.chess_id) for r in self.rounds for match in r.matches}

        # Initialize sets to track pairs and matches for the current round.
        paired_players = set()
        current_round_matches = []
        current_round = Round(f"Round {self.current_round}")

        # Loop through players and pair them if they haven't been paired before.
        for i, player1 in enumerate(self.players):
            if player1.chess_id in paired_players:
                continue
            for _, player2 in enumerate(self.players[i + 1:], start=i + 1):
                if (
                    (player2.chess_id in paired_players)
                    or ((player1.chess_id, player2.chess_id) in played_matches)
                    or ((player2.chess_id, player1.chess_id) in played_matches)
                ):
                    continue

                current_round_matches.append((player1, player2))
                paired_players.update([player1.chess_id, player2.chess_id])
                break

        # Create Match objects for each pair and add them to the current round.
        for player1, player2 in current_round_matches:
            current_round.add_match(Match(player1, player2))

        return current_round, current_round_matches

    def shuffle_players(self) -> None:
        """Randomly shuffles the list of players, usually done before the first round."""
        random.shuffle(self.players)

    def player_sort_key(self, player: Player) -> tuple:
        """Returns a tuple that is used as the sort key in sorting players, sorted by total points and then by ID."""
        total_points = self.get_player_points(player)
        return (-total_points, player.chess_id)

    def is_ended(self) -> bool:
        """Determines if the tournament has finished either by completing the designated number of rounds or if no more
        matches can be formed."""
        if len(self.rounds) >= self.round_number:
            return True
        _, pairs = self.generate_round_pairs()
        return len(pairs) == 0

    def __str__(self) -> str:
        """Provides a human-readable string representation of the tournament."""
        return (
            f"Tournament: {self.name}, Location: {self.location}, "
            f"Start Date: {self.start_date}, End Date: {self.end_date}, "
            f"Current Round: {self.current_round}, Max Rounds: {self.round_number}, "
            f"Description: {self.description}"
        )

    def to_dict(self) -> dict:
        """Serializes the Tournament object to a dictionary for storage or transmission.

        This method is typically used for saving the state of the tournament to a file
        or sending over a network in a format that can be easily converted to JSON.

        Returns:
            dict: A dictionary representation of the tournament with all its current state data.
        """
        # Create a base dictionary with the tournament's metadata.
        tournament_dict = {
            "name": self.name,  # Name of the tournament
            "location": self.location,  # Physical location of the tournament
            "start_date": self.start_date,  # Starting date of the tournament
            "end_date": self.end_date,  # Ending date of the tournament
            "description": self.description,  # Description of the tournament
            "round_number": self.round_number,  # Total number of rounds in the tournament
            "current_round": self.current_round,  # Current round number
            # Convert each player to a dictionary; good for JSON serialization
            "players": [player.to_dict() for player in self.players],
            "rounds": [],  # Initialize rounds as an empty list to be filled next
        }

        # Iterate over each round in the tournament.
        for round in self.rounds:
            # Create a dictionary to represent the round.
            round_dict = {
                "name": round.name,  # Name of the round
                "matches": [],  # Initialize matches as an empty list to be filled
                "is_finished": round.is_finished,  # Boolean indicating if the round is finished
            }

            # Iterate over each match in the round.
            for match in round.matches:
                # Convert the match to a dictionary using its own to_dict method.
                match_dict = match.to_dict()
                # Append the match dictionary to the round's list of matches.
                round_dict["matches"].append(match_dict)

            # Append the fully constructed round dictionary to the tournament's list of rounds.
            tournament_dict["rounds"].append(round_dict)

        return tournament_dict  # Return the complete tournament dictionary.

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Creates a Tournament object from a dictionary representation. This method is typically used when loading a
        tournament from a saved state, such as a JSON file.

        Args:
            data (dict): A dictionary containing all the tournament information.

        Returns:
            Tournament: A tournament object populated with the data from the dictionary.
        """
        # Create a new Tournament object with basic information from the dictionary.
        tournament = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data.get("description", ""),
            round_number=data.get("round_number", 4),
        )

        # Set the current round of the tournament, defaulting to 1 if not specified.
        tournament.current_round = data.get("current_round", 1)

        # Clear any existing players and rounds before populating from the loaded data.
        tournament.players = []  # Reset the players list.
        tournament.rounds = []  # Reset the rounds list.

        # Add players to the tournament from the 'players' data.
        # Each player is created using the Player.from_dict method.
        for player_data in data.get("players", []):
            player = Player.from_dict(player_data)
            tournament.players.append(player)

        # Add rounds and their matches to the tournament from the 'rounds' data.
        # Each round is created using the Round.from_dict method.
        for round_data in data.get("rounds", []):
            round = Round.from_dict(round_data)
            round.matches = []  # Reset the matches list for the round.

            # For each match in the round, find the players by their ID,
            # and create a Match object with the retrieved players and scores.
            for match_data in round_data["matches"]:
                player1 = tournament.find_player_by_id(match_data["player1"]["chess_id"])
                player2 = tournament.find_player_by_id(match_data["player2"]["chess_id"])
                match = Match(player1, player2)
                match.score1 = match_data["score1"]
                match.score2 = match_data["score2"]

                # Set the total points accumulated by each player up to this match.
                match.total_points_player1 = match_data.get("total_points_player1", 0)
                match.total_points_player2 = match_data.get("total_points_player2", 0)
                round.matches.append(match)

            # Add the fully constructed round to the tournament's list of rounds.
            tournament.rounds.append(round)

        return tournament  # Return the fully reconstructed Tournament object.

    def find_player_by_id(self, chess_id: str) -> Player:
        """Searches for a player in the tournament by their chess ID and returns the Player object."""
        for player in self.players:
            if player.chess_id == chess_id:
                return player
        raise ValueError(f"Player with ID {chess_id} not found in tournament.")

    def is_valid_player_count(self) -> bool:
        """Checks if the number of players in the tournament is even, which is required for pairing."""
        return len(self.players) % 2 == 0

    def has_duplicate_players(self) -> bool:
        """Checks for duplicate player entries based on chess ID, which should be unique."""
        ids = [player.chess_id for player in self.players]
        return len(ids) != len(set(ids))
