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
