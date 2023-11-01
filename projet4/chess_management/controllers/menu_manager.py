from views import tournament_view


class MenuManager:
    """
    Manages the interaction between the user and the tournament menu.
    
    Attributes:
        controller: The main application controller.
        tournament_view (tournament_view.TournamentView): The view to display the tournament form.
    """

    def __init__(self, controller):
        self.controller = controller
        self.tournament_view = tournament_view.TournamentView(self.controller)

    def create_tournament_form(self) -> None:
        """Displays the form to create a new tournament."""
        self.tournament_view.display_tournament_form()