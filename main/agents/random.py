import random
from typing import TYPE_CHECKING, Optional

from colorist import red

from main.types import Change
from main.utils import cprint

from .agent import Agent

if TYPE_CHECKING:
    from main.pieces import Piece


class RandomAgent(Agent):
    def _random_move(self, piece: "Piece") -> Optional[Change]:
        valid_moves = piece.get_valid_moves()
        captures = piece.get_captures(valid_moves)
        legal_moves = list(valid_moves | captures)

        if not legal_moves:
            return None

        pick = random.sample(legal_moves, 1)[0]
        if pick in piece.opponent.positions | {piece.opponent.en_passant_target}:
            cprint(self.color, f"{piece} capturing on {pick}", color_fn=red)
        else:
            cprint(self.color, f"Moving {piece} to {pick}")

        return piece.move(*pick)

    def move(self):
        for _, piece in sorted(self.pieces, key=lambda x: random.random()):
            if result := self._random_move(piece) is None:
                continue  # Piece is unmovable
            else:
                return result
