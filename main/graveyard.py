from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional

from main import constants
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn

if TYPE_CHECKING:
    from main.pieces.piece import Piece


@dataclass
class Graveyard:
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

    a_prom: Optional["Piece"] = None
    b_prom: Optional["Piece"] = None
    c_prom: Optional["Piece"] = None
    d_prom: Optional["Piece"] = None
    e_prom: Optional["Piece"] = None
    f_prom: Optional["Piece"] = None
    g_prom: Optional["Piece"] = None
    h_prom: Optional["Piece"] = None

    def __repr__(self):
        return "".join(f"  {piece}\n" for piece in self.pieces) or "  Empty"

    @property
    def pieces(self) -> Iterable["Piece"]:
        for name in self.piece_attrs:
            piece = getattr(self, name)
            if piece is not None:
                yield piece
