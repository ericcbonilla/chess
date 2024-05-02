from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main.pieces import Piece


# TODO abc - abstract class
@dataclass(kw_only=True)
class Processor:
    white: List["Piece"] = field(default_factory=list)
    black: List["Piece"] = field(default_factory=list)

    def __post_init__(self):
        self._convert()

    def _convert(self):
        raise NotImplementedError
