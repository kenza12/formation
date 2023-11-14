from views import user_view
from models.player import Player
from utils.load_data import load_state
import os


class UserManager:
    """Manages the interaction between the user and the player management functionalities.

    Attributes:
        controller: The main application controller.
        user_view (user_view.UserView): The view for player-related operations.
    """

    def __init__(self, controller):
        self.controller = controller
        self.user_view = user_view.UserView(self.controller)

    def register_player(self, **kwargs) -> None:
        """Registers a new player and associates them with a tournament if one exists."""
        player = Player(**kwargs)

        # Check if a tournament exists before adding the player
        if self.controller.tournament_manager.tournament is not None:
            self.controller.tournament_manager.tournament.add_player(player)
        else:
            print("No tournament has been created. Please create a tournament before adding players.")

    def display_registration_form(self) -> None:
        """Displays the form for player registration."""
        self.user_view.display_player_form()

    def display_player_submenu(self) -> None:
        """Displays the submenu related to player operations."""
        self.user_view.display_player_submenu()

    def modify_player(self) -> None:
        """Modifies the details of a specific player.

        (Functionality not yet implemented)
        """
        pass

    def display_player_list(self) -> None:
        """Displays player lists from the current tournament."""
        self.user_view.display_player_list()

    def get_all_players(self):
        """Retrieves and returns a list of player data from all tournaments in the specified directory.

        Returns:
        list: A list of dictionaries containing player information with keys 'first_name',
              'last_name', 'birthdate', and 'chess_id'.
        """
        players = []
        tournaments_path = "data/tournaments"
        for filename in os.listdir(tournaments_path):
            if filename.endswith(".json"):
                tournament = load_state(filename)
                if tournament:
                    for player in tournament.players:
                        player_data = {
                            "first_name": player.first_name,
                            "last_name": player.last_name,
                            "birthdate": player.birthdate,
                            "chess_id": player.chess_id,
                        }
                        players.append(player_data)
        return players

    def display_all_player_list(self):
        """Call the view method to display all players"""
        self.user_view.display_all_player_list()
