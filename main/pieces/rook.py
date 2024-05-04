from typing import TYPE_CHECKING, Optional

from main import constants
from main.types import Change
from main.xposition import XPosition

from .piece import Piece

if TYPE_CHECKING:
    from main.agents import Agent


class Rook(Piece):
    movements = {
        *((p, 0) for p in range(1, 9)),
        *((-p, 0) for p in range(1, 9)),
        *((0, p) for p in range(1, 9)),
        *((0, -p) for p in range(1, 9)),
    }
    symbol = "R"
    value = 5
    unicode = "\u2656"

    def __init__(
        self,
        attr: str,
        agent: "Agent",
        opponent: "Agent",
        x: str,
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(attr, agent, opponent, x, y)

        if has_moved is None:
            initial_y = 1 if self.agent.color == constants.WHITE else 8
            self.has_moved = self.position not in [("a", initial_y), ("h", initial_y)]
        else:
            self.has_moved = has_moved

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        if not self.has_moved:
            change[self.agent.color][self.attr]["has_moved"] = True

        return change
