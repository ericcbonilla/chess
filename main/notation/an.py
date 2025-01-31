import re
from typing import TYPE_CHECKING, Type

from main.exceptions import NotationError
from main.pieces import SYMBOLS_MAP, Pawn
from main.types import Position, Promotee, X
from main.x import C, G, to_int

if TYPE_CHECKING:
    from main.pieces import Piece


class AN:
    def __init__(self, text: str):
        self.text = text
        self.match = re.match(
            r""
            r"((?P<castle>^O-O-O|O-O)"  # Castle
            r"|(((?P<symbol>^[RBNKQ])"  # Piece symbol
            r"|(?P<pfile>^[a-h]))?"  # Attacking pawn file
            r"(?P<disamb>[a-h]?[1-8]?)?"  # Disambiguation
            r"(?P<capture>x)?"  # Capture
            r"(?P<pick>[a-h][1-8])"  # New position (pick)
            r"(?P<promotee>=[RBNQ])?))"  # Promotee symbol
            r"(?P<check>\+$)?"  # Check
            r"(?P<checkmate>#$)?",  # Checkmate
            string=text,
        )

        if self.match is None:
            raise NotationError(f'"{text}" is invalid algebraic notation')
        elif "=" in self.text and self.promotee_type is None:
            raise NotationError("Invalid promotee value, must be one of B, N, R, or Q")

    @property
    def piece_type(self) -> Type["Piece"]:
        symbol = self.match.group("symbol")
        if symbol is None and self.pick:
            return Pawn
        elif self.match.group("castle"):
            symbol = "K"

        return SYMBOLS_MAP[symbol]

    @property
    def pawn_file(self) -> X | None:
        if self.match.group("pfile"):
            return to_int(self.match.group("pfile"))

    @property
    def disambiguation(self) -> X | int | Position | None:
        disamb = self.match.group("disamb")
        if disamb == "" or disamb is None:
            return None
        if re.match(r"[a-h]$", disamb):
            return to_int(disamb)
        elif re.match(r"[1-8]$", disamb):
            return int(disamb)
        else:
            x_str, y = disamb
            return to_int(x_str), int(y)

    @property
    def is_capture(self) -> bool:
        return bool(self.match.group("capture"))

    @property
    def x(self) -> X:
        try:
            x_str, _ = self.match.group("pick")
            x = to_int(x_str)
        except TypeError:
            x = C if self.match.group("castle") == "O-O-O" else G

        return x

    @property
    def y(self) -> int | None:
        try:
            _, y = self.match.group("pick")
            return int(y)
        except TypeError:
            return None

    @property
    def pick(self) -> Position | None:
        if self.x and self.y:
            return self.x, self.y

    @property
    def promotee_type(self) -> Type[Promotee] | None:
        if promotee_symbol := self.match.group("promotee"):
            return SYMBOLS_MAP.get(promotee_symbol[-1])

    @property
    def check(self) -> bool:
        return bool(self.match.group("checkmate")) or bool(self.match.group("check"))

    @property
    def checkmate(self) -> bool:
        return bool(self.match.group("checkmate"))
