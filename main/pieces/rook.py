from typing import TYPE_CHECKING, Optional, Set, Tuple

from main import constants
from main.types import Change, Position
from main.utils import vector
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
    fen_symbol = symbol
    value = 5
    unicode = "\u2656"

    def __init__(
        self,
        attr: str,
        agent: "Agent",
        x: str,
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(attr, agent, x, y)

        if has_moved is None:
            initial_y = 1 if self.agent.color == constants.WHITE else 8
            self.has_moved = self.position not in [("a", initial_y), ("h", initial_y)]
        else:
            self.has_moved = has_moved

    def is_valid_vector(self, new_position: Position) -> bool:
        return 0 in vector(self.position, new_position)

    def _movements(self) -> Set[Tuple[int, int]]:

        # TODO start here, implement this for bishop and queen and then see if its worth it
        movements = set()
        x, y = self.position
        x.wrap = True

        for d in range(1, 8):
            movements.add((x.to_int() + d, y))
            movements.add((x.to_int(), ((y + d) % 8) or 8))
        x.wrap = False

        return movements

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        if not self.has_moved:
            change[self.agent.color][self.attr]["has_moved"] = True

        return change
