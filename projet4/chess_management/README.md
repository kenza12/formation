# Chess Management

## Description

The **Chess Tournament Manager** is a Python application that facilitates the organization of chess tournaments through the Swiss system. It offers a user-friendly graphical interface for entering player and tournament information, recording player scores for each round, saving and loading the tournament state for future continuation, and viewing tournament reports.

## Installation

Before running the application, ensure you have Python 3 installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

### Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/kenza12/formation.git
cd formation/projet4/chess_management
```

### Dependencies

This application uses only the Python standard library, so there are no external dependencies to install.

## Running the Application

To run the Chess Tournament Manager, use the following command:

```bash
python3 chess_management.py
```

## Using the Application

Once the application is running, you can:

1. Initiate a new tournament under `Tournament management`. Click on `Create New Tournament` and complete the required fields by clicking on `Submit`. You can view the tournament details by clicking on `View Tournament Details`.
2. Add players under `Player management`. You must first create a tournament in step 1 before registering players. Click `Register a new player` as needed to add all participants, fill in the required fields, and then select `List all players` to see the list of players registered for the current tournament.
3. After creating a new tournament and registering players or loading a tournament through `Load a tournament`, begin the tournament by selecting `Start a tournament`. Enter the player scores for each Round (1 pt for a win, 0 pt for a loss, 0.5 pt for a draw). The results, along with the updated scores and the start and end times of the round, will be displayed after scoring. You can choose not to proceed to the next Round and save the tournament's current state by clicking on `Save a tournament` to continue later.
4. As mentioned in step 3, you can save the current state of the tournament by clicking `Save a tournament` at any round you wish. The save files will be stored in the `data/tournaments` directory in JSON format.
5. Load a saved tournament from `data/tournaments` to continue or to view a particular tournament report by clicking on `Load a tournament` and selecting the relevant file.
6. Access reports of a loaded tournament or all created tournaments by clicking `View reports`:
    6.1. `List of all players in all tournaments` displays the roster of players from all previously created tournaments without needing to load them.
    6.2. `List of players in the active tournament` shows the list of players in the ongoing tournament. Load the tournament or create a new one and register players before using this feature.
    6.3. `View active tournament details` provides information about the ongoing tournament. Similar to step 6.2, you must load or create the tournament anew before selection.
    6.4. `View all tournaments details` reveals the details of all previously created tournaments. There is no need to load anything; if tournaments are found in `data/tournaments`, they will be displayed.
    6.5. `View active rounds and matches` presents all the rounds and matches of the current (or loaded) tournament. Of course, the rounds must have been played to show the results.

The GUI will guide you through the necessary steps to manage your tournament efficiently.

Please note that the `Modify Tournament Details` and `Edit a player` features are not implemented yet.

## Generating flake8 HTML report

To generate a flake8 HTML report for code quality checks, you will need to have `flake8` and the `flake8-html` plugin installed. If you haven't installed them yet, you can do so by running:

```bash
pip install flake8 flake8-html
```

After installing, you can generate the report by running:

```bash
flake8 --format=html --htmldir=flake8-report
```

The report will be generated in the `flake8-report` directory. Open the `index.html` file in a web browser to view it.
