import re

def add_to_dict(d, key, value):
    if key in d:
        d[key] += value
    else:
        d[key] = value

# Immutable snapshot of a player in this part
class Player:
    def __init__(self, position, score = 0):
        self.position = position
        self.score = score

    def move(self, units):
        new_position = ((self.position + units - 1) % 10) + 1
        new_score = self.score + new_position

        return Player(new_position, new_score)

    def __eq__(self, other):
        return self.score == other.score and self.position == other.position

    def __hash__(self):
        return hash((self.score, self.position))

# Immutable snapshot of a game in this part
class Game:
    def __init__(self, players):
        self.players = players

    def turn(self, player, roll):
        new_player = self.players[player].move(roll)

        new_players = (new_player, self.players[1]) if player == 0 else (self.players[0], new_player)

        return Game(new_players)

    def winner(self):
        if self.players[0].score >= 21:
            return 0
        elif self.players[1].score >= 21:
            return 1

    def loser(self):
        winner = self.winner()
        return 0 if winner == 1 else 1

    def __hash__(self):
        return hash(self.players)

    def __eq__(self, other):
        return self.players == other.players

# Parse input and create game
input = open("input.txt", "r")
player_1_position = int(re.search(r"Player 1 starting position: (\d)", input.readline())[1])
player_2_position = int(re.search(r"Player 2 starting position: (\d)", input.readline())[1])

# Create the inital game
game = Game((Player(player_1_position), Player(player_2_position)))

# The wins each player has
wins = [0, 0]

# The unvierses, indexed by the game state
universes: dict[Game, int] = {
    game: 1
}

# Whos turn it is
player_turn = 0

# This is how a 3 sided dice, rolled 3 times distrubutes itself among the possibilites
total_roll_dist = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

# While there are universes to be resolved
while len(universes) > 0:
    new_universes: dict[Game, int] = {}

    # For each game
    for game in universes:
        # For each dice possibility
        for total_roll in total_roll_dist:
            # Get the game that comes from the roll
            new_game = game.turn(player_turn, total_roll)

            # Get the winner
            winner = new_game.winner()

            # Get the total number of unverses created with this state
            total_universes = total_roll_dist[total_roll] * universes[game]

            if winner is None:
                # If there is no winner, add it back to be re evaluated
                add_to_dict(new_universes, new_game, total_universes)
            else:
                # Else, add it to wins
                wins[winner] += total_universes

    # Update whos turn it is
    player_turn = 1 if player_turn == 0 else 0

    universes = new_universes

# Print the win number of the player with the most wins
print(max(wins))
