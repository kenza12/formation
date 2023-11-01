from tkinter import Tk
from controllers import application_controller


class MainApplication:

    def __init__(self, root):
        self.controller = application_controller.ApplicationController(root)

    def run(self):
        self.controller.run()


if __name__ == "__main__":
    root = Tk()
    root.title("Chess Tournament Manager")
    app = MainApplication(root)
    app.run()