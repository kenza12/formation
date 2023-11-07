# Chess Management

## Description

Chess Tournament Manager is a Python application designed to help manage chess tournaments using the Swiss system. It provides a graphical user interface to input player details, pair players, and keep track of scores and rankings.

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

1. Create a new tournament with Tournament management.
2. Register players with Player management.
3. Start a tournament.
4. Save a tournament at any round.
5. Load a tournament at any round.
6. View reports.

The GUI will guide you through each step required to manage the tournament.

Note that `Modify Tournament Details` and `Edit a player` buttons are not yet implemented.

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
