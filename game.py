from board import *


class Game:
    def __init__(self):
        self.board = Board()
        self.age = 0

    def next_generation(self):
        new_board = copy.deepcopy(self.board)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.board.get_next_cell(i, j)
                new_board.init_cell(i, j, cell[0], cell[1], cell[2], cell[3])

        self.board = new_board
        self.age += 1

    def next_amount_of_generations(self, amount: int):
        for i in range(amount):
            self.next_generation()
