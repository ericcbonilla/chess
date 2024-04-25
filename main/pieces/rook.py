from typing import TYPE_CHECKING, Optional, Union

from main import constants
from main.types import Change
from main.xposition import XPosition

from .piece import Piece

if TYPE_CHECKING:
    from main.board import Board
    from main.team import Team


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
        board: "Board",
        team: "Team",
        x: Union[XPosition, str],
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(board, team, x, y)

        if has_moved is None:
            initial_y = 1 if self.team.color == constants.WHITE else 8
            self.has_moved = self.position not in [("a", initial_y), ("h", initial_y)]
        else:
            self.has_moved = has_moved

    def augment_change(
        self, x: Union[XPosition, str], y: int, change: Change, **kwargs
    ) -> Change:
        if not self.has_moved:
            change[self.team.color][self.name]["has_moved"] = True

        return change
