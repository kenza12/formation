from models.player import Player
from models.round import Round
from models.tournament import Tournament

# Création de quelques joueurs
player1 = Player("ID001", "John", "Doe", "1990-05-15")
player2 = Player("ID002", "Jane", "Smith", "1985-03-20")
player3 = Player("ID003", "Bob", "Johnson", "1995-08-10")
player4 = Player("ID004", "Alice", "Brown", "1988-12-05")

# Création d'un tournoi
tournament = Tournament("Chess Tournament", "City Chess Club", "2023-04-01", "2023-04-15", "Spring Chess Event")

# Ajout de joueurs au tournoi
tournament.add_player(player1)
tournament.add_player(player2)
tournament.add_player(player3)
tournament.add_player(player4)

# Création de Round 1
round1 = Round("Round 1")

# Démarrage de Round 1
round1.start_round()

# Ajout de matchs à Round 1
round1.add_match([player1.get_full_name(), player2.get_full_name()], [1, 0])
round1.add_match([player3.get_full_name(), player4.get_full_name()], [0, 1])

# Fin de Round 1
round1.end_round()

# Détails de Round 1
print("Détails de Round 1:")
print(round1)
for match in round1.matches:
    print(f"Match: {match[0]} - Scores: {match[1]}")

# Attribution de points pour Round 1
for match in round1.matches:
    player_names, scores = match
    for i, player_name in enumerate(player_names):
        for player in [player1, player2, player3, player4]:
            if player.get_full_name() == player_name:
                player.add_points(scores[i])


# Affichage des joueurs et de leurs points après Round 1
print("\nAprès Round 1:")
print(player1)
print(player2)
print(player3)
print(player4)

# Ajout de Round 1 au tournoi
tournament.rounds.append(round1)

# Création de Round 2
round2 = Round("Round 2")

# Démarrage de Round 2
round2.start_round()

# Ajout de matchs à Round 2
# Les gagnants du Round 1 jouent contre les gagnants, et les perdants contre les perdants
# John Doe contre Bob Johnson, Jane Smith contre Alice Brown
round2.add_match([player1.get_full_name(), player4.get_full_name()], [1, 0])
round2.add_match([player2.get_full_name(), player3.get_full_name()], [0, 1])

# Fin de Round 2
round2.end_round()

# Détails de Round 2
print("\nDétails de Round 2:")
print(round2)
for match in round2.matches:
    print(f"Match: {match[0]} - Scores: {match[1]}")

# Attribution de points pour Round 2
for match in round2.matches:
    player_names, scores = match
    for i, player_name in enumerate(player_names):
        for player in [player1, player2, player3, player4]:
            if player.get_full_name() == player_name:
                player.add_points(scores[i])

# Affichage des joueurs et de leurs points après Round 2
print("\nAprès Round 2:")
print(player1)
print(player2)
print(player3)
print(player4)

# Ajout de Round 2 au tournoi
tournament.rounds.append(round2)

# Mettre à jour l'attribut Current Round
tournament.current_round += 1

# Affichage du tournoi et de ses détails
print("\nDétails du tournoi:")
print(tournament)
for round in tournament.rounds:
    print("\nDétails du round:")
    print(round)
