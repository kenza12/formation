from models.tournament import Tournament


class TournamentManager:
    """
    Manages the main functionalities related to tournaments.

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
        """Starts the tournament if validation checks pass."""
        if self.validate_tournament():
            self.initiate_next_round()

    def validate_tournament(self) -> bool:
        """Validates if the tournament has correct details."""
        # Check if the tournament exists
        if not self.tournament:
            print("No tournament has been created. Please create one first.")
            return False

        # Validate player count in the tournament
        if not self.tournament.is_valid_player_count():
            print("Invalid number of players. Ensure you have an even number of players.")
            return False

        return True

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

        # Update players' scores
        for match in current_round.matches:
            self.controller.user_manager.update_player_scores(match)

        # After updating scores, check if the round is finished
        if current_round.is_finished:
            current_round.end_round()

        # Display results of the current round
        self.controller.menu_manager.tournament_view.display_round_results(current_round, start_time=current_round.start_time, end_time=current_round.end_time)

        if self.tournament.is_ended():
            self.controller.menu_manager.tournament_view.display_ended_tournament()
            return
        else:
            next_round = self.controller.menu_manager.tournament_view.ask_for_next_round()
            if next_round:
                self.initiate_next_round()
            else:
                print("Tournament paused.")


    def resume_tournament(self) -> None:
        """Resumes a paused or a saved tournament."""
        if not self.tournament:
            print("No tournament loaded.")
            return
        if self.tournament.is_ended():
            print("The tournament is already over.")
            self.controller.menu_manager.tournament_view.display_ended_tournament()
            return

        # Check if the rounds list is empty
        if not self.tournament.rounds:
            print("No round has been played yet. Please start the tournament.")
            return

        current_round = self.tournament.rounds[-1]
        if current_round.is_finished:
            print("The last round has ended. Please start the next round manually.")
        else:
            self.update_round_with_view()

    def display_all_players(self) -> None:
        """Displays the list of players in the current tournament."""
        if not self.tournament:
            print("No ongoing tournament. Please create one before listing the players.")
            return
        self.controller.menu_manager.user_view.display_players(self.tournament.players)
