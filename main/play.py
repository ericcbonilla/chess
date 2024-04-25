import os
import random
from colorist import yellow

from main import constants
from main.board import Board
from main.team import Team

term_size = os.get_terminal_size()


class Game:
    max_moves = 50  # Number of halfmoves is double this

    def __init__(self, board: Board):
        self.board = board

    def move(self, team: Team):
        raise NotImplementedError


class RandomGame(Game):
    # TODO Should we unify this with Board?

    def move(self, team: Team):
        for piece in sorted(team.values(), key=lambda x: random.random()):
            result = piece.random_move()
            if result is None:
                continue  # Piece is unmovable
            else:
                return result
        else:
            print("Stalemate/checkmate!")
            return None

    def play(self):
        move_count = 1

        while move_count <= self.max_moves and not self.board.result:
            print(f"{move_count}. {'=' * (term_size.columns - len(str(move_count)) - 2)}")
            print(f'Turn: {constants.WHITE}')
            self.move(self.board.white)

            yellow(f'Turn: {constants.BLACK}')
            self.move(self.board.black)
            print('')

            move_count += 1
