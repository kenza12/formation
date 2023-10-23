class Match:
    def __init__(self, player1, player2, score1=None, score2=None):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def __str__(self):
        return f"{self.player1.first_name} {self.player1.last_name} vs {self.player2.first_name} {self.player2.last_name} - Scores: {self.score1}-{self.score2}"