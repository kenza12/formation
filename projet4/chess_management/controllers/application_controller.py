from views import main_menu_view
from controllers import menu_manager, user_manager, tournament_manager
from utils import save_data, load_data


class ApplicationController:
    """
    Manages the main application functionalities such as menu, users, and tournaments.
    
    Attributes:
        root: The main application root or window.
        menu_manager (menu_manager.MenuManager): Manages the application menus.
        user_manager (user_manager.UserManager): Manages user interactions.
        tournament_manager (tournament_manager.TournamentManager): Manages tournament interactions.
        main_menu (main_menu_view.MainMenuView): The main application menu.
    """

    def __init__(self, root):  
        """
        Initializes an ApplicationController instance.
        
        Args:
            root: The main application root or window.
        """
        self.root = root

        # Initialize the managers before the main menu
        self.menu_manager = menu_manager.MenuManager(self)
        self.user_manager = user_manager.UserManager(self)
        self.tournament_manager = tournament_manager.TournamentManager(self)

        # Initialize the main menu after initializing the managers
        self.main_menu = main_menu_view.MainMenuView(self)

    def run(self) -> None:
        """Starts the main menu of the application."""
        self.main_menu.run()

    def create_tournament(self, **kwargs) -> None:
        """
        Creates a new tournament.

        Args:
            **kwargs: Keyword arguments to provide tournament details.
        """
        self.tournament_manager.create_tournament(**kwargs)

    def save_tournament(self) -> None:
        """Saves the current tournament's state."""
        save_data.save_tournament(self.tournament_manager.tournament)

    def load_tournament(self, file_name: str) -> None:
        """
        Loads a tournament's state from a given file.
        
        Args:
            file_name (str): The name/path of the file to load the tournament from.
        """
        tournament = load_data.load_state(file_name)
        if tournament:
            # If a valid tournament is loaded, resume it
            self.tournament_manager.tournament = tournament
            self.tournament_manager.resume_tournament()

    def register_player(self, **kwargs) -> None:
        """
        Registers a new player to the application.
        
        Args:
            **kwargs: Keyword arguments to provide player details.
        """
        self.user_manager.register_player(**kwargs)