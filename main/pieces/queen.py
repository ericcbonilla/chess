from .bishop import Bishop
from .piece import Piece
from .rook import Rook


class Queen(Piece):
    movements = Bishop.movements | Rook.movements
    capture_movements = movements
    symbol = "Q"
    fen_symbol = symbol
    value = 9
    unicode = "\u2655"
