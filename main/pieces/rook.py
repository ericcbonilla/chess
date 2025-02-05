from typing import TYPE_CHECKING, Optional

from main import constants
from main.pieces.utils import vector
from main.types import Change, Position, X
from main.x import A, H

from .piece import Piece

if TYPE_CHECKING:
    from main.agents import Agent


class Rook(Piece):
    movements = [
        [(p, 0) for p in range(1, 9)],
        [(-p, 0) for p in range(1, 9)],
        [(0, p) for p in range(1, 9)],
        [(0, -p) for p in range(1, 9)],
    ]
    symbol = "R"
    fen_symbol = symbol
    value = 5
    unicode = "\u2656"

    def __init__(
        self,
        attr: str,
        agent: "Agent",
        x: X,
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(attr, agent, x, y)

        if has_moved is None:
            initial_y = 1 if self.agent.color == constants.WHITE else 8
            self.has_moved = self.position not in {(A, initial_y), (H, initial_y)}
        else:
            self.has_moved = has_moved

    def is_valid_vector(self, new_position: Position) -> bool:
        return 0 in vector(self.position, new_position)

    def augment_change(self, x: X, y: int, change: Change, **kwargs) -> Change:
        if not self.has_moved:
            change[self.agent.color][self.attr]["has_moved"] = True

        return change
