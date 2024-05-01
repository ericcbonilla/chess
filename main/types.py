from typing import (
    TYPE_CHECKING,
    Dict,
    Literal,
    NotRequired,
    Tuple,
    Type,
    TypedDict,
    Union,
)

if TYPE_CHECKING:
    from main.pieces import Piece

Position = Tuple["XPosition", int]
Promotee = Union["Bishop", "Knight", "Queen", "Rook"]
TeamType = Dict[str, "Piece"]
TeamColor = Literal["WHITE", "BLACK"]
GameResult = Literal["", "1-0", "0-1", "½-½"]


class PieceChange(TypedDict):
    old_position: Position | None
    new_position: Position | None
    has_moved: NotRequired[bool]
    piece_type: NotRequired[Type["Piece"]]


TeamChange = Dict[str, PieceChange | Tuple[Position, None]]


class Change(TypedDict):
    WHITE: TeamChange
    BLACK: TeamChange
    disambiguation: NotRequired[str]
    check: NotRequired[bool]
    game_result: NotRequired[str]
