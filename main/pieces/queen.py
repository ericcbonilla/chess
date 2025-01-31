from main.pieces.utils import vector
from main.types import Position

from .bishop import Bishop
from .piece import Piece
from .rook import Rook


class Queen(Piece):
    movements = Bishop.movements | Rook.movements
    symbol = "Q"
    fen_symbol = symbol
    value = 9
    unicode = "\u2655"

    def is_valid_vector(self, new_position: Position) -> bool:
        x, y = vector((self.x, self.y), new_position)
        return x == y or 0 in (x, y)
