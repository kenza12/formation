import tkinter as tk
from tkinter import messagebox


class UserView:
    def __init__(self, controller) -> None:
        """
        Initialize the UserView.

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
        self.controller.register_player(chess_id=chess_id, first_name=first_name, last_name=last_name, birthdate=birthdate)

        # Close the secondary window
        self.form_window.destroy()

    def show_error(self, message: str) -> None:
        """Display an error message."""
        messagebox.showerror("Error", message)

    def display_player_submenu(self) -> None:
        """Display a submenu for player management."""
        self.submenu_window = tk.Toplevel(self.controller.root)
        self.submenu_window.title("Player Management")

        tk.Button(self.submenu_window, text="Register a new player", command=self.controller.user_manager.display_registration_form).pack(pady=10)
        tk.Button(self.submenu_window, text="List all players", command=self.display_player_list).pack(pady=10)
        tk.Button(self.submenu_window, text="Edit a player", command=self.controller.user_manager.modify_player).pack(pady=10)
        tk.Button(self.submenu_window, text="Return", command=self.submenu_window.destroy).pack(pady=10)

    def display_player_list(self) -> None:
        """Display the list of players in the active tournament, sorted alphabetically."""
        if not self.controller.tournament_manager.tournament:
            print("No ongoing tournament. Please create one before listing players.")
            return

        # Create a new window to show the player list
        self.list_window = tk.Toplevel(self.controller.root)
        self.list_window.title("List of players")

        # Create a Text widget to display player details
        player_text = tk.Text(self.list_window, wrap=tk.WORD, width=50, height=10)
        player_text.pack(padx=10, pady=10)

        # Get the list of players and sort it alphabetically
        sorted_players = sorted(self.controller.tournament_manager.tournament.players, 
                                key=lambda player: player.last_name)

        for player in sorted_players:
            player_details = str(player)
            player_text.insert(tk.END, player_details + "\n\n")

        # Button to close the window
        close_button = tk.Button(self.list_window, text="Close", command=self.list_window.destroy)
        close_button.pack(pady=10)