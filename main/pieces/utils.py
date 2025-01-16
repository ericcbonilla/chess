from typing import Tuple

from main.types import Position


def vector(position: Position, other: Position) -> Tuple[int, int]:
    x, y = position
    other_x, other_y = other

    return abs(x.to_int() - other_x.to_int()), abs(y - other_y)
