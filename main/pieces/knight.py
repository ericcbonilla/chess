from main.pieces.utils import vector
from main.types import Position

from .piece import Piece


class Knight(Piece):
    movements = [
        [(2, 1)],
        [(1, 2)],
        [(2, -1)],
        [(1, -2)],
        [(-2, 1)],
        [(-1, 2)],
        [(-2, -1)],
        [(-1, -2)],
    ]
    capture_movements = movements
    symbol = "N"
    fen_symbol = symbol
    value = 3
    unicode = "\u2658"

    def is_valid_vector(self, new_position: Position) -> bool:
        return vector(self.position, new_position) in [(1, 2), (2, 1)]

    def is_valid_move(self, new_position: Position) -> bool:
        if not self.is_valid_movement(new_position):
            return False
        elif self.king_would_be_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        return True
