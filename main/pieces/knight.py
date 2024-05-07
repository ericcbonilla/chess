from typing import Optional

from main import constants
from main.types import Position

from .piece import Piece


class Knight(Piece):
    movements = {(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)}
    capture_movements = movements
    symbol = "N"
    value = 3
    unicode = "\u2658"

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.forbidden_squares
            or self.king_is_in_check(king=self.king, new_position=new_position)
        ):
            return False
        return True
