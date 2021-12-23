import re

class Dice:
    def get_times_rolled(self):
        return 1

    def roll(self):
        return 1

class DetDice(Dice):
    def __init__(self):
        self.value = 1
        self.times_rolled = 0

    def roll(self):
        store_value = self.value

        self.value = (self.value % 100) + 1
        self.times_rolled += 1

        return store_value
    
    def get_times_rolled(self):
        return self.times_rolled

class Player:
    def __init__(self, position):
        self.score = 0
        self.position = position

    def move(self, units):
        self.position = ((self.position + units - 1) % 10) + 1
    
    def add_to_score(self):
        self.score += self.position

class Game:
    def __init__(self, dice, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.players_turn = self.p1

        self.dice = dice

    def turn(self):
        players_turn = self.players_turn
        self.players_turn = self.p1 if players_turn == self.p2 else self.p2

        total_of_rolls = sum(list(map(lambda _: self.dice.roll(), [None] * 3)))

        players_turn.move(total_of_rolls)
        players_turn.add_to_score()

    def winner(self):
        if self.p1.score >= 1000:
            return self.p1
        elif self.p2.score >= 1000:
            return self.p2

    def loser(self):
        winner = self.winner()
        if winner == self.p1:
            return self.p2
        elif winner == self.p2:
            return self.p1

    def score(self):
        loser = self.loser()

        return loser.score * self.dice.get_times_rolled()

# Parse input and create game
input = open("input.txt", "r")
player_1_position = int(re.search(r"Player 1 starting position: (\d)", input.readline())[1])
player_2_position = int(re.search(r"Player 2 starting position: (\d)", input.readline())[1])

game = Game(DetDice(), Player(player_1_position), Player(player_2_position))

# Play the game
while game.winner() == None:
    game.turn()

# Print the score
print(game.score())
