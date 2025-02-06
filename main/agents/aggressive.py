import random
from typing import Optional

from main.game_tree import HalfMove
from main.types import X

from .random import RandomAgent


class AggressiveAgent(RandomAgent):
    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[X] = None,
        y: Optional[int] = None,
    ) -> Optional[HalfMove]:
        """
        Priotize in this order:
            1. Checks
            2. Captures
            3. Regular moves
        """

        pieces = list(self.pieces.values())
        for piece in sorted(pieces, key=lambda _: random.random()):
            for cand in piece.get_valid_moves():
                if piece.king_would_be_in_check(piece.opponent.king, cand):
                    return piece.move(*cand, check=True)
                elif cand in piece.opponent.pieces:
                    return piece.move(*cand)

        return super().move(attr=attr, x=x, y=y)
