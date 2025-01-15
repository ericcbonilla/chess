from typing import Set, Tuple

from main.types import Position
from main.utils import vector

from .piece import Piece


class Bishop(Piece):
    movements = {
        *((p, p) for p in range(1, 9)),
        *((p, -p) for p in range(1, 9)),
        *((-p, p) for p in range(1, 9)),
        *((-p, -p) for p in range(1, 9)),
    }
    symbol = "B"
    fen_symbol = symbol
    value = 3
    unicode = "\u2657"

    def is_valid_vector(self, new_position: Position) -> bool:
        x, y = vector(self.position, new_position)
        return x == y

    def _movements(self) -> Set[Tuple[int, int]]:
        movements = set()
        x, y = self.position
        x.wrap = True

        for d in range(1, 8):
            movements.add((x + d, ((y + d) % 8) or 8))
        x.wrap = False

        return movements
