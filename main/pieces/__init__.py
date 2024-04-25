# Order matters here - else circular imports occur
from .pawn import WhitePawn, BlackPawn
from .bishop import Bishop
from .king import King
from .knight import Knight
# from .piece import Piece
from .queen import Queen
from .rook import Rook
