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

        pieces = list(self.pieces.values())
        for piece in sorted(pieces, key=lambda _: random.random()):
            for move in piece.get_valid_moves():
                if piece.king_would_be_in_check(piece.opponent.king, move):
                    cprint(f"Turn: {self.color}", self.color)
                    if (
                        move in piece.opponent.pieces
                        or move == piece.opponent.en_passant_target
                    ):
                        cprint(f"{piece} capturing on {move}", self.color, color_fn=red)
                    else:
                        cprint(f"Moving {piece} to {move}", self.color)
                    return piece.move(*move)
                elif move in piece.opponent.pieces:
                    cprint(f"Turn: {self.color}", self.color)
                    cprint(f"{piece} capturing on {move}", self.color, color_fn=red)

                    return piece.move(*move)

        return super().move(attr=attr, x=x, y=y)
