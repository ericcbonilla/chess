"""
Order matters here - else circular imports occur
isort:skip_file
"""

from .piece import Piece
from .pawn import WhitePawn, BlackPawn, Pawn
from .bishop import Bishop
from .king import King
from .knight import Knight
from .queen import Queen
from .rook import Rook


SYMBOLS_MAP = {
    "P": WhitePawn,
    "p": BlackPawn,
    "r": Rook,
    "R": Rook,
    "n": Knight,
    "N": Knight,
    "b": Bishop,
    "B": Bishop,
    "k": King,
    "K": King,
    "q": Queen,
    "Q": Queen,
}
