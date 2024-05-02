from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from main import constants

from .processor import Processor

if TYPE_CHECKING:
    from main.pieces import Piece


@dataclass(kw_only=True)
class CollectionProcessor(Processor):
    coll: List["Piece"]

    def _convert(self):
        for piece in self.coll:
            if piece.color == constants.WHITE:
                self.white.append(piece)
            else:
                self.black.append(piece)
