from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Set

from main import constants
from main.agents.graveyard import Graveyard
from main.exceptions import NotFoundError
from main.game_tree import HalfMove
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn
from main.types import AgentColor, Position, Promotee, X

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

    # Caches of the pieces and their positions
    # Stays updated to the current halfmove
    pieces_cache: Dict[Position, "Piece"] = field(default_factory=dict)

    def __repr__(self):
        return f'{self.color} {type(self)}:\n{"".join(f"  {p.attr}: {p}\n" for p in self.pieces.values())}'

    @property
    def positions(self) -> Set[Position]:
        return set(self.pieces.keys())

    def del_cache_item(self, key: Position):
        try:
            del self.pieces_cache[key]
        except KeyError:
            pass

    def cache_pieces(self):
        # TODO likely some other ways we can leverage this now that we have
        # O(1) access to pieces

        self.pieces_cache = {}
        for attr in constants.PIECE_ATTRS:
            if piece := getattr(self, attr):
                self.pieces_cache[(piece.x, piece.y)] = piece

    @property
    def pieces(self) -> Dict[Position, "Piece"]:
        if self.pieces_cache:
            return self.pieces_cache

        self.cache_pieces()
        return self.pieces_cache

    @property
    def material_sum(self) -> int:
        return sum(self.material)

    @property
    def material(self) -> List[int]:
        return [piece.value for piece in self.pieces.values()]

    @property
    def castling_rights(self) -> str:
        rights = ""
        if not self.king.has_moved:
            if self.h_rook and not self.h_rook.has_moved:
                rights += "K"
            if self.a_rook and not self.a_rook.has_moved:
                rights += "Q"

        return rights

    def get_by_position(self, x: X, y: int) -> "Piece":
        try:
            return self.pieces[(x, y)]
        except KeyError:
            raise NotFoundError(f"Piece not found on {(x, y)}")

    def get_bishop(self) -> Bishop:
        for piece in self.pieces.values():
            if isinstance(piece, Bishop):
                return piece

        raise NotFoundError("Bishop not found")

    def can_move(self) -> bool:
        pieces = list(self.pieces.values())

        for piece in pieces:
            if piece.can_move():
                return True

        return False

    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[X] = None,
        y: Optional[int] = None,
    ) -> Optional[HalfMove]:
        """
        Make a move based on my strategy
        """

        raise NotImplementedError
