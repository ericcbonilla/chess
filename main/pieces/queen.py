from .bishop import Bishop
from .piece import Piece
from .rook import Rook


class Queen(Piece):
    movements = Bishop.movements | Rook.movements
    symbol = "Q"
    value = 9
    unicode = "\u2655"
