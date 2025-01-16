from typing import TYPE_CHECKING

from main import constants
from main.pieces.utils import vector
from main.types import Position

from .piece import Piece

if TYPE_CHECKING:
    from main.agents import Agent


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

    def __init__(self, attr: str, agent: "Agent", x: str, y: int):
        super().__init__(attr, agent, x, y)
        self.dark = self.position in constants.DARK_SQUARES

    def is_valid_vector(self, new_position: Position) -> bool:
        x, y = vector(self.position, new_position)
        return x == y
