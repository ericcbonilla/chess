from main.types import Position
from main.utils import vector

from .piece import Piece


class Bishop(Piece):
    movements = {
        *((p, p) for p in range(1, 9)),
        *((p, -p) for p in range(1, 9)),
        *((-p, p) for p in range(1, 9)),
        *((-p, -p) for p in range(1, 9)),
    }
    symbol = "B"
    fen_symbol = symbol
    value = 3
    unicode = "\u2657"

    def is_valid_vector(self, new_position: Position) -> bool:
        x, y = vector(self.position, new_position)
        return x == y
