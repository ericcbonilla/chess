import random
from typing import Optional

from colorist import red

from main.game_tree import HalfMove
from main.utils import cprint

from .random import RandomAgent


class AggressiveAgent(RandomAgent):
    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[str] = None,
        y: Optional[int] = None,
    ) -> Optional[HalfMove]:
        """
        Priotize in this order:
            1. Checks
            2. Captures
            3. Regular moves
        """

        for _, piece in sorted(self.pieces, key=lambda _: random.random()):
            for move in piece.get_valid_moves():
                if piece.king_would_be_in_check(piece.opponent.king, move):
                    cprint(f"Turn: {self.color}", self.color)
                    if move in piece.opponent.positions | {
                        piece.opponent.en_passant_target
                    }:
                        cprint(f"{piece} capturing on {move}", self.color, color_fn=red)
                    else:
                        cprint(f"Moving {piece} to {move}", self.color)
                    return piece.move(*move)

        for _, piece in sorted(self.pieces, key=lambda _: random.random()):
            if captures := piece.get_captures(valid_moves=piece.get_valid_moves()):
                pick = random.sample(sorted(captures), 1)[0]
                cprint(f"Turn: {self.color}", self.color)
                cprint(f"{piece} capturing on {pick}", self.color, color_fn=red)

                return piece.move(*pick)

        return super().move(attr=attr, x=x, y=y)
