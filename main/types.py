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
AgentColor = Literal["WHITE", "BLACK"]
GameResult = Literal[
    None,
    "1-0",
    "0-1",
    "½-½ Stalemate",
    "½-½ Insufficient material",
    "½-½ Seventy-five-move rule",
]


class PieceChange(TypedDict):
    old_position: Position | None
    new_position: Position | None
    has_moved: NotRequired[bool]
    piece_type: NotRequired[Type["Piece"]]


AgentChange = Dict[str, PieceChange | Tuple[Position, None]]


class Change(TypedDict):
    WHITE: AgentChange
    BLACK: AgentChange
    disambiguation: NotRequired[str]
    check: NotRequired[bool]
    game_result: NotRequired[GameResult]
    symbol: str | None


class PieceScaffold(TypedDict):
    piece_type: Type["Piece"]
    x: str
    y: int
    has_moved: NotRequired[bool]


AgentScaffold = Dict[str, PieceScaffold | None]
