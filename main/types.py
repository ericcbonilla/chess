from typing import (TYPE_CHECKING, Dict, Literal, NotRequired, Tuple,
                    TypedDict, Union)

if TYPE_CHECKING:
    from main.pieces import (Bishop, BlackPawn, King, Knight, Queen, Rook,
                             WhitePawn)

Position = Tuple['XPosition', int]
PieceType = Union['Bishop', 'King', 'Knight', 'WhitePawn', 'BlackPawn', 'Queen', 'Rook']
TeamType = Dict[str, PieceType]
TeamColor = Literal['WHITE', 'BLACK']
GameResult = Literal['', '1-0', '0-1', '½-½']


class PieceChange(TypedDict):
    old_position: Position | None
    new_position: Position | None
    has_moved: NotRequired[bool]
    piece_type: NotRequired[PieceType]


TeamChange = Dict[str, PieceChange | Tuple[Position, None]]


class Change(TypedDict):
    WHITE: TeamChange
    BLACK: TeamChange
    disambiguation: NotRequired[str]
    check: NotRequired[bool]
    game_result: NotRequired[str]
