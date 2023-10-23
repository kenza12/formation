import random
from models.player import Player


class Tournament:
    def __init__(self, name: str, location: str, start_date: str, end_date: str, description: str = "", round_number: int = 4, current_round: int = 1, rounds: list = None, players: list = None):
        """
        Initialize a Tournament instance.

        :param name: The name of the tournament (str).
        :param location: The location of the tournament (str).
        :param start_date: The start date of the tournament (str).
        :param end_date: The end date of the tournament (str).
        :param description: A description of the tournament (str, default is an empty string).
        :param round_number: The total number of rounds in the tournament (int, default is 4).
        :param current_round: The current round of the tournament (int, default is 1).
        :param rounds: A list to store the rounds of the tournament (list, default is an empty list).
        :param players: A list to store the players participating in the tournament (list, default is an empty list).
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.current_round = current_round
        self.description = description
        self.rounds = rounds or []
        self.players = players or []

    def add_player(self, player: Player):
        """
        Add a player to the tournament.

        :param player: The player to add to the tournament (Player).
        """
        self.players.append(player)

    def shuffle_players(self):
        """
        Shuffle all registered players in the tournament randomly.
        """
        random.shuffle(self.players)

    def __str__(self):
        """
        Return a string representation of the Tournament instance.

        :return: A string describing the tournament, including its name, location, start date, end date, current round, maximum rounds, and description.
        """
        return f"Tournament: {self.name}, Location: {self.location}, Start Date: {self.start_date}, End Date: {self.end_date}, Current Round: {self.current_round}, Max Rounds: {self.round_number}, Description: {self.description}"