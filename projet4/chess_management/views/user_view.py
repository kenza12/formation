import tkinter as tk
from tkinter import messagebox


class UserView:
    def __init__(self, controller) -> None:
        """Initialize the UserView.

        :param controller: Reference to the application controller.
        :type controller: Controller
        """
        self.controller = controller
        self.form_window: tk.Toplevel = None
        self.submenu_window: tk.Toplevel = None
        self.list_window: tk.Toplevel = None

    def display_player_form(self) -> None:
        """Display a form window to input player details."""
        # Create a window for player information entry
        self.form_window = tk.Toplevel(self.controller.root)
        self.form_window.title("Register a player")

        # Add fields to input player details
        tk.Label(self.form_window, text="Player ID:").pack(pady=10)
        self.chess_id_entry = tk.Entry(self.form_window)
        self.chess_id_entry.pack(pady=5)

        tk.Label(self.form_window, text="First Name:").pack(pady=10)
        self.first_name_entry = tk.Entry(self.form_window)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.form_window, text="Last Name:").pack(pady=10)
        self.last_name_entry = tk.Entry(self.form_window)
        self.last_name_entry.pack(pady=5)

        tk.Label(self.form_window, text="Birthdate:").pack(pady=10)
        self.birthdate_entry = tk.Entry(self.form_window)
        self.birthdate_entry.pack(pady=5)

        # Submit button for details
        tk.Button(self.form_window, text="Submit", command=self.submit_player_form).pack(pady=20)

    def submit_player_form(self) -> None:
        """Retrieve and process inputted player details, then register player via the controller."""
        # Fetch the inputted details
        chess_id = self.chess_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        birthdate = self.birthdate_entry.get()

        # Check if all fields are filled
        if not (chess_id and first_name and last_name and birthdate):
            self.show_error("All fields are required!")
            return

        # Use the details to register a player through the controller
        self.controller.register_player(
            chess_id=chess_id,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
        )

        # Close the secondary window
        self.form_window.destroy()

    def show_error(self, message: str) -> None:
        """Display an error message."""
        messagebox.showerror("Error", message)

    def display_player_submenu(self) -> None:
        """Display a submenu for player management."""
        self.submenu_window = tk.Toplevel(self.controller.root)
        self.submenu_window.title("Player Management")

        tk.Button(
            self.submenu_window,
            text="Register a new player",
            command=self.controller.user_manager.display_registration_form,
        ).pack(pady=10)
        tk.Button(
            self.submenu_window,
            text="List all players",
            command=self.display_player_list,
        ).pack(pady=10)
        tk.Button(
            self.submenu_window,
            text="Edit a player",
            command=self.controller.user_manager.modify_player,
        ).pack(pady=10)
        tk.Button(self.submenu_window, text="Return", command=self.submenu_window.destroy).pack(pady=10)

    def display_player_list(self) -> None:
        """Display the list of players in the active tournament, sorted alphabetically."""
        if not self.controller.tournament_manager.tournament:
            messagebox.showinfo("Information", "No ongoing tournament. Please create one before listing players.")
            return

        # Create a new window to show the player list
        self.list_window = tk.Toplevel(self.controller.root)
        self.list_window.title("List of players")

        # Create a frame to contain the Text widget and Scrollbar
        frame = tk.Frame(self.list_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a Text widget to display player details
        player_text = tk.Text(frame, wrap=tk.NONE, font=("Helvetica", 11))
        player_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # Horizontal scrollbar
        xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=player_text.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        player_text['xscrollcommand'] = xscrollbar.set

        # Configure the "bold" style tag
        player_text.tag_configure("bold", font=("Helvetica", 11, "bold"))

        # Get the list of players and sort it alphabetically
        sorted_players = sorted(
            self.controller.tournament_manager.tournament.players,
            key=lambda player: player.last_name.lower(),
        )

        for player in sorted_players:
            player_text.insert(tk.END, "• Player: ", "bold")
            player_text.insert(tk.END, f"{player.last_name} {player.first_name} - ")
            player_text.insert(tk.END, "Chess ID: ", "bold")
            player_text.insert(tk.END, f"{player.chess_id} - ")
            player_text.insert(tk.END, "Birthdate: ", "bold")
            player_text.insert(tk.END, f"{player.birthdate}\n")

        # Prevent the user from modifying the text and add a button to close the window
        player_text.config(state=tk.DISABLED)
        tk.Button(self.list_window, text="Close", command=self.list_window.destroy).pack(pady=10)

    def display_all_player_list(self) -> None:
        """Affiche la liste des joueurs de tous les tournois, triée par ordre alphabétique."""
        try:
            players = self.controller.user_manager.get_all_players()  # Récupère les données de tous les joueurs
            sorted_players = sorted(
                players, key=lambda player: player["last_name"].lower()
            )  # Trier par nom de famille

            # Créer une nouvelle fenêtre pour afficher la liste des joueurs
            self.list_window = tk.Toplevel(self.controller.root)
            self.list_window.title("List of all players in all tournaments")

            # Créer un widget Text pour afficher les détails des joueurs avec une meilleure mise en forme
            player_text = tk.Text(self.list_window, wrap=tk.NONE, font=("Helvetica", 11))
            player_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Configure le style "bold" pour le tag
            player_text.tag_configure("bold", font=("Helvetica", 11, "bold"))

            # Insertion des détails de chaque joueur avec une puce devant
            for player in sorted_players:
                player_title = "• Player: "
                player_text.insert(tk.END, player_title, "bold")
                player_details = f"{player['last_name']} {player['first_name']} - "
                player_text.insert(tk.END, player_details)

                # Ajoute "Chess ID" en gras, suivi de sa valeur
                chess_id_text = "Chess ID: "
                player_text.insert(tk.END, chess_id_text, "bold")
                player_text.insert(tk.END, f"{player['chess_id']} - ")

                # Ajoute "Birthdate" en gras, suivi de sa valeur
                birthdate_text = "Birthdate: "
                player_text.insert(tk.END, birthdate_text, "bold")
                player_text.insert(tk.END, f"{player['birthdate']}\n")

            # Empêcher l'utilisateur de modifier le texte
            player_text.config(state=tk.DISABLED)

            # Bouton pour fermer la fenêtre
            close_button = tk.Button(self.list_window, text="Fermer", command=self.list_window.destroy)
            close_button.pack(pady=10)

        except Exception as e:
            self.show_error(f"Une erreur s'est produite lors de l'affichage des joueurs : {e}")
