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

X = int
Position = Tuple[X, int]
Vector = Tuple[int, int]
Promotee = Union["Bishop", "Knight", "Queen", "Rook"]
AgentColor = Literal["WHITE", "BLACK"]
GameResult = Literal[
    None,
    "1-0",
    "0-1",
    "½-½ Stalemate",
    "½-½ Insufficient material",
    "½-½ Repetition",
    "½-½ Seventy-five-move rule",
]


class PieceChange(TypedDict):
    old_position: Position | None
    new_position: Position | None
    has_moved: NotRequired[bool]
    piece_type: NotRequired[Type["Piece"]]


AgentChange = Dict[str, PieceChange | Tuple[Position, None]]


class LookaheadResults(TypedDict):
    check: NotRequired[bool]
    game_result: NotRequired[GameResult]
    fen: NotRequired[str]


class Change(LookaheadResults):
    WHITE: AgentChange
    BLACK: AgentChange
    disambiguation: NotRequired[str]
    rows_changing: NotRequired[set]
    symbol: str | None
    halfmove_clock: Tuple[int, int]
    fullmove_number: Tuple[int, int]


class PieceScaffold(TypedDict):
    piece_type: Type["Piece"]
    x: int
    y: int
    has_moved: NotRequired[bool]


AgentScaffold = Dict[str, PieceScaffold | None]
