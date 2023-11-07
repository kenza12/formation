import tkinter as tk
from tkinter import messagebox, font


class TournamentView:
    """Handles the GUI view for the tournament operations."""

    def __init__(self, controller):
        """
        Initialize the TournamentView.

        :param controller: The main application controller
        """
        self.controller = controller
        self.form_window = None
        self.submenu_window = None
        self.details_window = None
        self.round_window = None
        self.next_round_window = None
        self.ended_tournament_window = None

    def display_tournament_form(self) -> None:
        """Display the form to gather tournament details."""
        # Create window for tournament details input
        self.form_window = tk.Toplevel(self.controller.root)
        self.form_window.title("Create a new tournament")

        # Add fields for tournament details input
        fields = ["Tournament Name:", "Location:", "Start Date:", "End Date:", "Description:", "Number of Rounds:"]
        self.entries = {}
        for field in fields:
            tk.Label(self.form_window, text=field).pack()
            entry = tk.Entry(self.form_window)
            entry.pack()
            self.entries[field] = entry

        # Submit button
        tk.Button(self.form_window, text="Submit", command=self.submit_tournament_form).pack()

    def submit_tournament_form(self) -> None:
        """Retrieve input details and create a new tournament."""
        # Fetch details from input fields
        name = self.entries["Tournament Name:"].get()
        location = self.entries["Location:"].get()
        start_date = self.entries["Start Date:"].get()
        end_date = self.entries["End Date:"].get()
        description = self.entries["Description:"].get()
        rounds = int(self.entries["Number of Rounds:"].get()) if self.entries["Number of Rounds:"].get().isdigit() else 0

        # Use controller to create the tournament
        self.controller.create_tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description,
            round_number=rounds
        )

        # Close the secondary window
        self.form_window.destroy()

    def display_tournament_submenu(self) -> None:
        """Display the submenu for tournament management."""
        self.submenu_window = tk.Toplevel(self.controller.root)
        self.submenu_window.title("Tournament Management")

        tk.Button(self.submenu_window, text="Create New Tournament", command=self.display_tournament_form).pack()
        tk.Button(self.submenu_window, text="Modify Tournament Details", command=self.modify_tournament).pack()
        tk.Button(self.submenu_window, text="View Tournament Details", command=self.display_tournament_details).pack()
        tk.Button(self.submenu_window, text="Return", command=self.submenu_window.destroy).pack()

    def display_reports_submenu(self) -> None:
        """Display the submenu for reports"""
        self.submenu_window = tk.Toplevel(self.controller.root)
        self.submenu_window.title("Reports")

        tk.Button(self.submenu_window, text="List of all players in all tournaments", command=self.controller.user_manager.display_all_player_list).pack()
        tk.Button(self.submenu_window, text="List of players in the active tournament", command=self.controller.user_manager.display_player_list).pack()
        tk.Button(self.submenu_window, text="View active tournament details", command=self.display_tournament_details).pack()
        tk.Button(self.submenu_window, text="View all tournaments details", command=self.controller.tournament_manager.display_all_tournaments).pack()
        tk.Button(self.submenu_window, text="View active rounds and matches", command=self.display_active_rounds_and_matches).pack()
        tk.Button(self.submenu_window, text="Return", command=self.submenu_window.destroy).pack()

    def modify_tournament(self) -> None:
        """Modify an existing tournament. (Functionality not yet implemented)"""
        pass

    def display_tournament_details(self) -> None:
        """Display the details of the tournament."""
        if not self.controller.tournament_manager.tournament:
            print("No tournament to display!")
            return

        self.details_window = tk.Toplevel(self.controller.root)
        self.details_window.title("Tournament Details")

        tournament = self.controller.tournament_manager.tournament

        # Create a Text widget for structured display
        details_text = tk.Text(self.details_window, wrap=tk.NONE, font=("Helvetica", 11))
        details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure bold style for titles
        details_text.tag_configure("bold", font=("Helvetica", 11, "bold"))

        # Inserting tournament details with titles in bold followed by values
        details_entries = [
            ("Name:", tournament.name),
            ("Location:", tournament.location),
            ("Start Date:", tournament.start_date),
            ("End Date:", tournament.end_date),
            ("Description:", tournament.description),
            ("Number of Rounds:", str(tournament.round_number))
        ]

        for title, value in details_entries:
            details_text.insert(tk.END, title, "bold")
            details_text.insert(tk.END, f" {value}\n")

        # Prevent user from editing the text
        details_text.config(state=tk.DISABLED)

        # Return button to close details window
        tk.Button(self.details_window, text="Return", command=self.details_window.destroy).pack(pady=10)

    def ask_match_scores(self, matches: list) -> dict:
        """
        Prompt the user to input scores for all matches in a given round.

        :param matches: List of match objects to gather scores for.
        :return: A dictionary containing matches as keys and scores as values.
        """
        
        # Retrieve the current round number
        current_round_number = len(self.controller.tournament_manager.tournament.rounds)

        # Create a new tkinter window to input scores
        scores_window = tk.Toplevel(self.controller.root)
        scores_window.title(f"Enter scores for Round {current_round_number}")

        self.score_entries = {}

        # For each match, create an input interface for scores
        for match in matches:
            frame = tk.Frame(scores_window)
            frame.pack(pady=10)

            # Player 1 score input
            player1_label = tk.Label(frame, text=f"{match.player1.get_full_name()}:")
            player1_label.grid(row=0, column=0)
            player1_score = tk.StringVar(value='0')
            player1_entry = tk.Spinbox(frame, from_=0, to=1, increment=0.5, textvariable=player1_score, width=5)
            player1_entry.grid(row=0, column=1)

            # "VS" label
            vs_label = tk.Label(frame, text="VS")
            vs_label.grid(row=0, column=2)

            # Player 2 score input
            player2_label = tk.Label(frame, text=f"{match.player2.get_full_name()}:")
            player2_label.grid(row=0, column=3)
            player2_score = tk.StringVar(value='0')
            player2_entry = tk.Spinbox(frame, from_=0, to=1, increment=0.5, textvariable=player2_score, width=5)
            player2_entry.grid(row=0, column=4)

            self.score_entries[match] = (player1_score, player2_score)

        # Submit button
        submit_button = tk.Button(scores_window, text="Submit", command=scores_window.destroy)
        submit_button.pack(pady=20)

        # Wait for the user to submit the scores
        scores_window.wait_window()

        scores = {}
        for match, (score1_var, score2_var) in self.score_entries.items():
            score1 = float(score1_var.get())
            score2 = float(score2_var.get())

            # Check if scores are valid
            if score1 not in [0, 0.5, 1] or score2 not in [0, 0.5, 1]:
                messagebox.showerror("Error", "Invalid scores. Only 0, 0.5, and 1 are allowed.")
                return self.ask_match_scores(matches)  # Ask for scores again if invalid

            scores[match] = (score1, score2)

        return scores

    def display_round_results(self, current_round, start_time=None, end_time=None) -> None:
        """
        Display the total points of players for the given round in a tkinter window.

        :param current_round: The round object whose results are to be displayed.
        :param start_time: The start time of the round.
        :param end_time: The end time of the round.
        """
        
        # Create a new tkinter window to display round results
        self.round_window = tk.Toplevel(self.controller.root)
        self.round_window.title(f"Results - {current_round.name}")

        # Display start_time and end_time if provided
        if start_time and end_time:
            bold_font = font.Font(family="Verdana", size=10, weight="bold")

            time_frame = tk.Frame(self.round_window)
            time_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5, columnspan=2)

            tk.Label(time_frame, text=f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", font=bold_font).grid(row=0, column=0, sticky="w", padx=(0, 20))
            tk.Label(time_frame, text=f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}", font=bold_font).grid(row=0, column=1, sticky="w")
            
        # Display results for each match in the round
        for i, match in enumerate(current_round.matches, start=1):
            points_player1 = self.controller.tournament_manager.tournament.get_player_points(match.player1)
            points_player2 = self.controller.tournament_manager.tournament.get_player_points(match.player2)

            label_text = f"{match.player1.get_full_name()}: {points_player1} points VS {match.player2.get_full_name()}: {points_player2} points"
            label = tk.Label(self.round_window, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5, columnspan=2)

        # Quit button to close the round results window
        quit_btn = tk.Button(self.round_window, text="Quit", command=self.quit_cmd)
        quit_btn.grid(row=i + 1, column=0, pady=10)

        # Wait for user action
        self.round_window.wait_window()

    def next_round_cmd(self):
        """Commande pour le bouton 'Prochain Tour'."""
        self.result = True  # utilisateur a choisi de passer au prochain tour
        self.round_window.destroy()
        self.round_window = None

    def quit_cmd(self):
        """Commande pour le bouton 'Quitter'."""
        self.result = False  # utilisateur a choisi de quitter
        self.round_window.destroy()
        self.round_window = None

    def display_ended_tournament(self):
        if not self.controller.tournament_manager.tournament:
            print("Aucun tournoi à afficher!")
            return

        if self.controller.tournament_manager.tournament.is_ended():
            messagebox.showinfo("Tournoi", "Le tournoi est terminé!")
            self.ended_tournament_window = tk.Toplevel(self.controller.root)
            self.ended_tournament_window.title("Détails du tournoi terminé")

            tournament = self.controller.tournament_manager.tournament

            tk.Label(self.ended_tournament_window, text=f"Nom: {tournament.name}").pack()
            tk.Label(self.ended_tournament_window, text=f"Lieu: {tournament.location}").pack()
            tk.Label(self.ended_tournament_window, text=f"Date de début: {tournament.start_date}").pack()
            tk.Label(self.ended_tournament_window, text=f"Date de fin: {tournament.end_date}").pack()
            tk.Label(self.ended_tournament_window, text=f"Description: {tournament.description}").pack()
            tk.Label(self.ended_tournament_window, text=f"Nombre de tours: {tournament.round_number}").pack()

            tk.Button(self.ended_tournament_window, text="Retour", command=self.ended_tournament_window.destroy).pack()

    def ask_for_next_round(self) -> bool:
        """Prompt user if they wish to proceed to the next round."""
        self.next_round_window = tk.Toplevel(self.controller.root)
        self.next_round_window.title("Continue the tournament")

        tk.Label(self.next_round_window, text="Do you want to proceed to the next round?").pack(pady=20)

        self.next_round_result = None

        tk.Button(self.next_round_window, text="Yes", command=self.next_round_yes_cmd).pack(side=tk.LEFT, padx=10)
        tk.Button(self.next_round_window, text="No", command=self.next_round_no_cmd).pack(side=tk.LEFT, padx=10)

        self.next_round_window.wait_window()  # Wait for user to make a choice

        return self.next_round_result

    def next_round_yes_cmd(self) -> None:
        """Handle the 'Yes' command for proceeding to the next round."""
        self.next_round_result = True
        self.next_round_window.destroy()

    def next_round_no_cmd(self) -> None:
        """Handle the 'No' command for not proceeding to the next round."""
        self.next_round_result = False
        self.next_round_window.destroy()

    def display_all_tournament_details(self, tournaments) -> None:
        """Display the details of all tournaments in a single window."""
        # Créer une fenêtre pour afficher les détails
        all_details_window = tk.Toplevel(self.controller.root)
        all_details_window.title("All Tournaments Details")

        # Créer un widget Text pour l'affichage structuré
        details_text = tk.Text(all_details_window, wrap=tk.NONE, font=("Helvetica", 11))
        details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configurer le style en gras pour les titres
        details_text.tag_configure("bold", font=("Helvetica", 11, "bold"))

        # Insérer les détails de chaque tournoi dans le widget Text
        for tournament in tournaments:
            details_entries = [
                ("Name:", tournament.name),
                ("Location:", tournament.location),
                ("Start Date:", tournament.start_date),
                ("End Date:", tournament.end_date),
                ("Description:", tournament.description),
                ("Number of Rounds:", str(tournament.round_number)),
                ("-"*40, "")  # Ligne de séparation
            ]

            for title, value in details_entries:
                details_text.insert(tk.END, title, "bold")
                details_text.insert(tk.END, f" {value}\n")

        # Empêcher l'utilisateur de modifier le texte
        details_text.config(state=tk.DISABLED)

        # Bouton de retour pour fermer la fenêtre
        tk.Button(all_details_window, text="Return", command=all_details_window.destroy).pack(pady=10)

    def display_active_rounds_and_matches(self) -> None:
        """Display the rounds and matches of the active tournament with updated total points."""
        tournament = self.controller.tournament_manager.tournament
        if not tournament or not tournament.rounds:
            messagebox.showinfo("Information", "No active rounds or matches to display.")
            return

        # Create a new tkinter window to display rounds and matches
        rounds_window = tk.Toplevel(self.controller.root)
        rounds_window.title("Active Rounds and Matches")

        # Utiliser un set pour suivre les matchs déjà affichés
        displayed_matches = set()

        # Afficher les matchs de chaque round
        for round in tournament.rounds:
            tk.Label(rounds_window, text=f"{round.name}:", font=("Helvetica", 11, "bold")).pack(anchor='w')
            
            for match in round.matches:
                # Récupérer les points totaux pour chaque joueur de tous les rounds précédents
                total_points_player1 = match.total_points_player1
                total_points_player2 = match.total_points_player2
                match_details = f"{match.player1.get_full_name()} ({total_points_player1} points) VS {match.player2.get_full_name()} ({total_points_player2} points)"
                
                # Vérifier si les détails du match sont déjà affichés pour éviter les doublons
                if match_details not in displayed_matches:
                    tk.Label(rounds_window, text=match_details).pack(anchor='w')
                    displayed_matches.add(match_details)

        # Close button to close the rounds and matches window
        tk.Button(rounds_window, text="Close", command=rounds_window.destroy).pack(pady=10)