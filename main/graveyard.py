from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional

from main import constants
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn
from main.types import Promotee

if TYPE_CHECKING:
    from main.pieces import Piece


@dataclass
class Graveyard:
    king: Optional[King] = None
    queen: Optional[Queen] = None
    a_rook: Optional[Rook] = None
    h_rook: Optional[Rook] = None
    b_knight: Optional[Knight] = None
    g_knight: Optional[Knight] = None
    c_bishop: Optional[Bishop] = None
    f_bishop: Optional[Bishop] = None

    a_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    b_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    c_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    d_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    e_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    f_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    g_slot: Optional[Promotee | WhitePawn | BlackPawn] = None
    h_slot: Optional[Promotee | WhitePawn | BlackPawn] = None

    def __repr__(self):
        return f'Graveyard:\n{"".join(f"  {p}\n" for p in self.pieces) or "  Empty"}'

    @property
    def pieces(self) -> Iterable["Piece"]:
        for name in constants.PIECE_ATTRS:
            piece = getattr(self, name)
            if piece is not None:
                yield piece
