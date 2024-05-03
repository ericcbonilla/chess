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
    from main.pieces.piece import Piece

Position = Tuple["XPosition", int]
Promotee = Union["Bishop", "Knight", "Queen", "Rook"]
AgentColor = Literal["WHITE", "BLACK"]
GameResult = Literal[None, "1-0", "0-1", "½-½"]


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
    game_result: NotRequired[GameResult]
