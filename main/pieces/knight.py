from typing import Optional

from main.types import Position

from .piece import Piece


class Knight(Piece):
    movements = {(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)}
    capture_movements = movements
    symbol = "N"
    fen_symbol = symbol
    value = 3
    unicode = "\u2658"

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if not self.is_valid_movement(new_position):
            return False
        elif keep_king_safe and self.king_would_be_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        return True
