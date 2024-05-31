from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, List, Optional, Set

from main import constants
from main.game_tree import HalfMove
from main.graveyard import Graveyard
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn
from main.types import AgentColor, Position, Promotee
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

    a_prom: Optional[Promotee] = None
    b_prom: Optional[Promotee] = None
    c_prom: Optional[Promotee] = None
    d_prom: Optional[Promotee] = None
    e_prom: Optional[Promotee] = None
    f_prom: Optional[Promotee] = None
    g_prom: Optional[Promotee] = None
    h_prom: Optional[Promotee] = None

    en_passant_target: Optional[Position] = None

    def __repr__(self):
        return f'{self.color}:\n{"".join(f"  {a}: {p}\n" for a, p in self.pieces)}'

    @property
    def pieces(self) -> Iterable["Piece"]:
        for attr in constants.PIECE_ATTRS:
            if piece := getattr(self, attr):
                yield attr, piece

    @property
    def material_sum(self) -> int:
        return sum(self.material)

    @property
    def material(self) -> List[int]:
        return [piece.value for _, piece in self.pieces]

    @property
    def positions(self) -> Set[Position]:
        return set(piece.position for _, piece in self.pieces)

    @property
    def castling_rights(self) -> str:
        rights = ""
        if not self.king.has_moved:
            if self.h_rook and not self.h_rook.has_moved:
                rights += "K"
            if self.a_rook and not self.a_rook.has_moved:
                rights += "Q"

        return rights

    def get_by_position(self, x: XPosition, y: int) -> "Piece":
        for _, piece in self.pieces:
            if piece.position == (x, y):
                return piece

        raise Exception(f"Piece not found on {(x, y)}")

    def can_move(self) -> bool:
        for _, piece in self.pieces:
            if piece.can_move():
                return True

        return False

    def move(self) -> Optional[HalfMove]:
        """
        Make a move based on my strategy
        """

        raise NotImplementedError
