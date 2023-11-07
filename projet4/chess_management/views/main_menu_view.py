import tkinter as tk
from tkinter import filedialog


class MainMenuView:
    def __init__(self, controller):
        """
        Initialize the main menu view.
        
        :param controller: The main controller object for the application.
        :type controller: Any
        """
        self.controller = controller
        self.root = controller.root
        self.initialize_view()

    def initialize_view(self) -> None:
        """Initialize the main menu buttons."""
        tk.Button(self.root, text="Player management", command=self.controller.user_manager.display_player_submenu).pack()
        tk.Button(self.root, text="Tournament management", command=self.controller.tournament_manager.display_tournament_submenu).pack()
        tk.Button(self.root, text="Start a tournament", command=self.controller.tournament_manager.start_tournament).pack()
        tk.Button(self.root, text="Save a tournament", command=self.controller.save_tournament).pack()
        tk.Button(self.root, text="Load a tournament", command=self.load_tournament_from_file).pack()
        tk.Button(self.root, text="View reports", command=self.controller.tournament_manager.display_reports_submenu).pack()
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()
    
    def load_tournament_from_file(self) -> None:
        """
        Open a file dialog to allow the user to select a tournament file and then load it.
        """
        file_path = filedialog.askopenfilename(title="Sélectionnez le fichier du tournoi", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.controller.load_tournament(file_path)

    def run(self) -> None:
        """Run the main tkinter loop."""
        self.root.mainloop()