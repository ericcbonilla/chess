from typing import Dict

from main.types import Position
from main.x import A, E, H, to_int


class FEN:
    def __init__(self, text: str):
        self._a, self._b, self._c, self._d, self._e, self._f = text.split(" ")

    @property
    def piece_placement(self) -> str:
        return self._a

    @property
    def active_color(self) -> str:
        return self._b

    @property
    def castling_rights(self) -> Dict[Position, bool]:
        return {
            (A, 8): "q" in self._c,
            (H, 8): "k" in self._c,
            (A, 1): "Q" in self._c,
            (H, 1): "K" in self._c,
            (E, 8): any(ch in self._c for ch in ("k", "q")),
            (E, 1): any(ch in self._c for ch in ("K", "Q")),
        }

    @property
    def en_passant_target(self) -> Position | None:
        try:
            x_str, y = self._d
            return to_int(x_str), int(y)
        except ValueError:
            return None

    @property
    def halfmove_clock(self) -> int:
        return int(self._e)

    @property
    def fullmove_number(self) -> int:
        return int(self._f)
