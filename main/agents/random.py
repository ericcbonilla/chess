import random
from typing import TYPE_CHECKING, Optional

from main.game_tree import HalfMove
from main.types import X

from .agent import Agent

if TYPE_CHECKING:
    from main.pieces import Piece


class RandomAgent(Agent):
    @staticmethod
    def _random_move(piece: "Piece") -> Optional[HalfMove]:
        moveset = list(piece.get_moveset())

        if not moveset:
            return None

        pick = random.sample(moveset, 1)[0]

        return piece.move(*pick)

    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[X] = None,
        y: Optional[int] = None,
    ) -> Optional[HalfMove]:
        pieces = list(self.pieces.values())
        for piece in sorted(pieces, key=lambda _: random.random()):
            if (result := self._random_move(piece)) is None:
                continue  # Piece is unmovable
            else:
                return result
