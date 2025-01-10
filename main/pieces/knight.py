from .piece import Piece


class Knight(Piece):
    movements = {(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)}
    capture_movements = movements
    symbol = "N"
    fen_symbol = symbol
    value = 3
    unicode = "\u2658"
