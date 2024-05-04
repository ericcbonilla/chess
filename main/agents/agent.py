from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, Optional, Set

from main import constants
from main.graveyard import Graveyard
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn
from main.types import AgentColor, Position
from main.xposition import XPosition

if TYPE_CHECKING:
    from main.board import Board
    from main.pieces import Piece


@dataclass
class Agent:
    """
    Responsibilities:
    - Game strategy (Compute my next move)
        - Requires a full view of the board including the opponent agent
    - Offer access to individual Pieces (dead or alive)
    - Offer access to set of all Pieces, set of positions
    """

    color: AgentColor
    board: "Board"
    graveyard: Graveyard = field(default_factory=Graveyard)
    piece_attrs = constants.PIECE_ATTRS

    king: Optional[King] = None
    queen: Optional[Queen] = None
    a_rook: Optional[Rook] = None
    h_rook: Optional[Rook] = None
    b_knight: Optional[Knight] = None
    g_knight: Optional[Knight] = None
    c_bishop: Optional[Bishop] = None
    f_bishop: Optional[Bishop] = None

    a_pawn: Optional[WhitePawn | BlackPawn] = None
    b_pawn: Optional[WhitePawn | BlackPawn] = None
    c_pawn: Optional[WhitePawn | BlackPawn] = None
    d_pawn: Optional[WhitePawn | BlackPawn] = None
    e_pawn: Optional[WhitePawn | BlackPawn] = None
    f_pawn: Optional[WhitePawn | BlackPawn] = None
    g_pawn: Optional[WhitePawn | BlackPawn] = None
    h_pawn: Optional[WhitePawn | BlackPawn] = None

    # TODO Can we unify this with pawn attrs?
    a_prom: Optional["Piece"] = None
    b_prom: Optional["Piece"] = None
    c_prom: Optional["Piece"] = None
    d_prom: Optional["Piece"] = None
    e_prom: Optional["Piece"] = None
    f_prom: Optional["Piece"] = None
    g_prom: Optional["Piece"] = None
    h_prom: Optional["Piece"] = None

    en_passant_target: Optional[Position] = None

    def __repr__(self):
        return "".join(f"  {piece}\n" for piece in self.pieces)

    @property
    def pieces(self) -> Iterable["Piece"]:
        for name in self.piece_attrs:
            piece = getattr(self, name)
            if piece is not None:
                yield piece

    @property
    def material(self) -> int:
        return sum([piece.value for piece in self.pieces])

    @property
    def positions(self) -> Set[Position]:
        return set(piece.position for piece in self.pieces)

    def get_by_position(self, x: XPosition, y: int) -> "Piece":
        for piece in self.pieces:
            if piece.position == (x, y):
                return piece

        raise Exception(f"Piece not found on {(x, y)}")

    def can_move(self) -> bool:
        for piece in self.pieces:
            if piece.can_move():
                return True

        return False

    def move(self):
        """
        Make a move based on my strategy
        """

        raise NotImplementedError
