from typing import TYPE_CHECKING, Optional, Set

# if TYPE_CHECKING:
from main.pieces import BlackPawn, WhitePawn
from main.types import PieceType, Position, TeamColor
from main.xposition import XPosition


class Team(dict):
    """
    3/22/24
    We used to store pieces in both a "registry" (set) and a "piece_map" (dict).
    It was inelegant to do this, essentially we were tracking the same things in two
    different places.

    This dict extension lets us only store pieces in one place (a "Team"), but we
    can still access them in a set whenever we need to elegantly express or compute
    something using set notation.
    """

    def __init__(self, color: TeamColor, en_passant_target: Optional[Position] = None):
        super().__init__()
        self.color = color
        self.en_passant_target = en_passant_target

    def __repr__(self):
        return ''.join(f'  {name}: {piece}\n' for name, piece in self.items())

    @property
    def material(self) -> int:
        return sum([piece.value for piece in self.values()])

    @property
    def positions(self) -> Set[Position]:
        return set(piece.position for piece in self.values())

    def get_by_position(self, x: XPosition, y: int) -> PieceType:
        for piece_name, piece in self.items():
            if piece.position == (x, y):
                return self[piece_name]

        raise Exception(f'Piece not found on {(x, y)}')

    def can_move(self) -> bool:
        for piece in self.values():
            if piece.can_move():
                return True

        return False
