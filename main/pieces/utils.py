from main.types import Position, Vector


def vector(position: Position, other: Position) -> Vector:
    x, y = position
    other_x, other_y = other

    return abs(x - other_x), abs(y - other_y)
