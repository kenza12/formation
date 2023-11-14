from models.tournament import Tournament
from utils.load_data import load_state
import os


class TournamentManager:
    """Manages the main functionalities related to tournaments.

    Attributes:
        controller: The main application controller.
        tournament (Tournament): The tournament object that will be managed.
    """

    def __init__(self, controller):
        self.controller = controller
        self.tournament = None  # This will be initialized when creating the tournament

    def display_tournament_submenu(self) -> None:
        """Displays the tournament submenu."""
        self.controller.menu_manager.tournament_view.display_tournament_submenu()

    def create_tournament(self, **kwargs) -> None:
        """Creates a new tournament instance."""
        self.tournament = Tournament(**kwargs)

    def start_tournament(self) -> None:
        """Starts or resumes a tournament based on its current state."""
        if not self.tournament:
            print("No tournament loaded. Please create a tournament first.")
            return

        if self.tournament.is_ended():
            print("The tournament is already over.")
            self.controller.menu_manager.tournament_view.display_ended_tournament()
            return

        # Starts the tournament if validation checks pass.
        if self.validate_tournament():
            self.initiate_next_round()

    def validate_tournament(self) -> bool:
        """Validates if the tournament has correct details."""
        valid = True  # Assume the tournament is valid to start with

        # Check if the tournament exists
        if not self.tournament:
            print("No tournament has been created. Please create one first.")
            valid = False
        # Validate player count in the tournament
        elif not self.tournament.is_valid_player_count():
            print("Invalid number of players. Ensure you have an even number of players.")
            valid = False
        # Check for duplicate players
        elif self.tournament.has_duplicate_players():
            print("Duplicate players detected. Each player must be unique.")
            valid = False

        return valid

    def initiate_next_round(self) -> None:
        """Starts a new round in the tournament."""
        self.tournament.start_new_round()
        self.update_round_with_view()

    def update_round_with_view(self) -> None:
        """Updates the round details and views accordingly."""
        current_round = self.tournament.rounds[-1]

        # Get match scores from the user
        scores = self.controller.menu_manager.tournament_view.ask_match_scores(current_round.matches)
        for match, (score1, score2) in scores.items():
            match.set_scores(score1, score2)
            # Update total points for each player in the match
            match.total_points_player1 = self.tournament.get_player_points(match.player1)
            match.total_points_player2 = self.tournament.get_player_points(match.player2)

        # After updating scores, check if the round is finished
        if current_round.is_finished:
            current_round.end_round()

        # Display results of the current round
        self.controller.menu_manager.tournament_view.display_round_results(current_round)

        # Check if the tournament has ended and display the appropriate view
        self.check_tournament_end()

    def check_tournament_end(self):
        """Check if the tournament has ended and display the appropriate view."""
        if self.tournament.is_ended():
            self.controller.menu_manager.tournament_view.display_ended_tournament()
        else:
            # Ask user if they want to proceed to the next round
            next_round = self.controller.menu_manager.tournament_view.ask_for_next_round()
            if next_round:
                self.initiate_next_round()
            else:
                print("Tournament paused.")

    def display_reports_submenu(self) -> None:
        """Displays the reports submenu."""
        self.controller.menu_manager.tournament_view.display_reports_submenu()

    def display_all_tournaments(self) -> None:
        """Fetch and display details of all tournaments in a single window."""
        # Retrieve all tournaments
        tournaments = []
        tournaments_files = os.listdir("data/tournaments")
        for file_name in tournaments_files:
            if file_name.endswith(".json"):
                tournament = load_state(file_name)
                if tournament:
                    tournaments.append(tournament)
                else:
                    print(f"Failed to load tournament from {file_name}")

        # Display all tournaments if the list is not empty
        if tournaments:
            self.controller.menu_manager.tournament_view.display_all_tournament_details(tournaments)
        else:
            print("Error", "No tournaments to display.")
