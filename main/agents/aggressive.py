import random
from typing import Optional

from colorist import red

from main.game_tree import HalfMove
from main.types import X
from main.utils import cprint

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
                check = piece.king_would_be_in_check(piece.opponent.king, cand)
                if check:
                    cprint(f"Turn: {self.color}", self.color)
                    if (
                        cand in piece.opponent.pieces
                        or cand == piece.opponent.en_passant_target
                    ):
                        cprint(f"{piece} capturing on {cand}", self.color, color_fn=red)
                    else:
                        cprint(f"Moving {piece} to {cand}", self.color)
                    return piece.move(*cand, check=True)
                elif cand in piece.opponent.pieces:
                    cprint(f"Turn: {self.color}", self.color)
                    cprint(f"{piece} capturing on {cand}", self.color, color_fn=red)

                    return piece.move(*cand)

        return super().move(attr=attr, x=x, y=y)
