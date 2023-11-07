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

    def add_player(self, player: Player) -> None:
        """Add a new player to the tournament and initialize the score to 0"""
        self.players.append(player)

    def get_player_points(self, player: Player) -> float:
        """Calculate the total points of a player by summing up the points from all matches."""
        total_points = 0
        for round in self.rounds:
            for match in round.matches:
                if match.player1 == player:
                    total_points += match.score1
                elif match.player2 == player:
                    total_points += match.score2
        return total_points

    def start_new_round(self):
        """Starts a new round in the tournament only if the previous one is finished or if there is no round yet."""
        if self.rounds and not self.rounds[-1].is_finished:
            print("The current round is not yet finished.")
            return
        
        if self.current_round == 1:
            self.shuffle_players()
        else:
            self.players.sort(key=lambda player: -self.get_player_points(player))
        
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
        """Sort key function for ordering players based on total points and IDs."""
        total_points = self.get_player_points(player)
        return (-total_points, player.chess_id)

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
        """Converts the tournament object to a dictionary, including total points per player per round."""
        tournament_dict = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "round_number": self.round_number,
            "current_round": self.current_round,
            "players": [player.to_dict() for player in self.players],
            "rounds": []
        }

        # Add rounds and matches information with updated total points
        for round in self.rounds:
            round_dict = {
                "name": round.name,
                "matches": [],
                "is_finished": round.is_finished
            }
            
            # Update each match with the total points of each player by that round
            for match in round.matches:
                match_dict = match.to_dict()
                round_dict['matches'].append(match_dict)
            
            tournament_dict['rounds'].append(round_dict)

        return tournament_dict

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Initializes a tournament from a dictionary representation, including previous rounds and scores."""
        tournament = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data.get("description", ""),
            round_number=data.get("round_number", 4)
        )
        tournament.current_round = data.get("current_round", 1)
        
        # Réinitialiser les joueurs et les rondes avant de les remplir avec les données chargées
        tournament.players = []
        tournament.rounds = []

        # Add players
        for player_data in data.get("players", []):
            player = Player.from_dict(player_data)
            tournament.players.append(player)
        
        # Add rounds and matches
        for round_data in data.get("rounds", []):
            round = Round.from_dict(round_data)
            round.matches = []  # Réinitialiser les matchs de la ronde avant de les remplir
            for match_data in round_data["matches"]:
                player1 = tournament.find_player_by_id(match_data["player1"]["chess_id"])
                player2 = tournament.find_player_by_id(match_data["player2"]["chess_id"])
                match = Match(player1, player2)
                match.score1 = match_data["score1"]
                match.score2 = match_data["score2"]
                match.total_points_player1 = match_data.get("total_points_player1", 0)
                match.total_points_player2 = match_data.get("total_points_player2", 0)
                round.matches.append(match)
            tournament.rounds.append(round)
        
        return tournament

    def find_player_by_id(self, chess_id: str) -> Player:
        """Finds a player in the tournament by their chess ID."""
        for player in self.players:
            if player.chess_id == chess_id:
                return player
        raise ValueError(f"Player with ID {chess_id} not found in tournament.")

    def is_valid_player_count(self) -> bool:
        """Checks if the number of players is even."""
        return len(self.players) % 2 == 0

    def has_duplicate_players(self) -> bool:
        """Checks for the presence of duplicate players in the tournament."""
        ids = [player.chess_id for player in self.players]
        return len(ids) != len(set(ids))
