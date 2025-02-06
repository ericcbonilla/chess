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
        valid_moves = list(piece.get_valid_moves())

        if not valid_moves:
            return None

        pick = random.sample(valid_moves, 1)[0]

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
