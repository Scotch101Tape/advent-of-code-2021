import re

class Board:
    winning_states = [
        {0, 1, 2, 3, 4}, 
        {5, 6, 7, 8, 9}, 
        {10, 11, 12, 13, 14}, 
        {15, 16, 17, 18, 19}, 
        {20, 21, 22, 23, 24}, 
        {0, 5, 10, 15, 20},
        {1, 6, 11, 16, 21}, 
        {2, 7, 12, 17, 22}, 
        {3, 8, 13, 18, 23}, 
        {4, 9, 14, 19, 24}, 
        {0, 6, 12, 18, 24}, 
        {4, 8, 12, 16, 20}]

    def __init__(self, string):
        self.board_numbers = list(map(lambda x: int(x), # map to ints
            list(filter(lambda x: x.isdigit(), # filter out only ones that are ints
            re.split(r" |\n", string))))) # parse the numbers by newline or space
        self.called = set() # the called on the board is a set

    def score(self, number):
        # filter out all the board numbers whose indexes are in called
        uncalled = list(filter(lambda x: not (self.board_numbers.index(x) in self.called), self.board_numbers)) 

        return number * sum(uncalled) # return the number times the sum of the uncalled numbers

    def add_number(self, number):
        if (number in self.board_numbers):
            self.called.add(self.board_numbers.index(number))

    def check_bingo(self):
        for state in Board.winning_states:
            if state.issubset(self.called):
                return True
        return False



input = open("input.txt", "r")

content = re.split(r"\n\n", input.read())

(numbers_called, board_strings) = (list(map(lambda x: int(x), re.split(r",", content[0]))), content[1:-1])

boards = list(map(lambda x: Board(x), board_strings))

def get_losing_score(boards):
    for number in numbers_called:
        new_boards = boards.copy()
        for board in boards:
            board.add_number(number)
            if board.check_bingo():
                new_boards.remove(board)
                if len(new_boards) == 0:
                    return board.score(number)
        boards = new_boards

print(get_losing_score(boards))