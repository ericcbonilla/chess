from typing import Set

from main.game_tree import HalfMove
from main.types import Change, Position
from main.utils import vector
from main.xposition import XPosition

from .piece import Piece
from .queen import Queen


class Pawn(Piece):
    symbol = ""
    fen_symbol = "P"
    value = 1
    capture_movements: Set = NotImplemented
    y_init: int = NotImplemented
    unicode = "\u2659"

    @property
    def forbidden_squares(self) -> Set[Position]:
        return self.agent.positions | self.opponent.positions

    def is_valid_vector(self, new_position: Position) -> bool:
        vec = vector(self.position, new_position)
        if self.y == self.y_init:
            return vec in [(0, 1), (0, 2), (1, 1)]
        return vec in [(0, 1), (1, 1)]

    def is_capture(self, new_position: Position) -> bool:
        # TODO fix XPosition off board idk why this is causing that though
        # Need to refactor movements so they don't even look at off board squares...
        # return vector(self.position, new_position) == (1, 1)

        return any(
            (self.x + x_d, self.y + y_d) == new_position
            for x_d, y_d in self.capture_movements
        )

    def is_valid_move(self, new_position: Position) -> bool:
        if self.is_capture(new_position):
            if new_position in self.opponent.positions | {
                self.opponent.en_passant_target
            }:
                if self.king_would_be_in_check(
                    king=self.king,
                    new_position=new_position,
                ):
                    return False
                return True
            return False

        return super().is_valid_move(new_position)

    def get_disambiguation(self, x: XPosition, y: int) -> str:
        return ""

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        change["halfmove_clock"] = (self.agent.board.halfmove_clock, 0)

        if (x, y) == self.opponent.en_passant_target:
            piece = self.opponent.get_by_position(x, self.y)
            change[self.opponent.color] = {
                piece.attr: {
                    "old_position": (x, self.y),
                    "new_position": None,
                }
            }

        if not self.is_promotion(y):
            return change

        if "promotee_type" not in kwargs:
            # If king_would_be_in_check is testing a promotion move, we must provide a piece type.
            # Just assume Queen in this case. Or, if a promotee_value is not provided,
            # also just assume Queen. You could play a decade of chess and never find a
            # situation where you need a Knight. This is fine for our purposes.
            promotee_type = Queen
        else:
            # Let's also assume that whatever client is sending the move knows
            # when it needs to supply a promotee_value
            promotee_type = kwargs["promotee_type"]

        change[self.agent.color][self.attr]["new_position"] = None
        change[self.agent.color][f"{self.attr[0]}_prom"] = {
            "old_position": None,
            "new_position": (x, y),
            "piece_type": promotee_type,
        }

        return change

    def set_en_passant_target(self, y: int):
        if abs(self.y - y) == 2:
            target_y = int((self.y + y) / 2)
            self.agent.en_passant_target = (self.x, target_y)

    def move(self, x: XPosition, y: int, **kwargs) -> HalfMove:
        self.set_en_passant_target(y=y)
        return super().move(x, y, **kwargs)

    @staticmethod
    def is_promotion(y: int) -> bool:
        return y in (1, 8)


class WhitePawn(Pawn):
    capture_movements = {(1, 1), (-1, 1)}
    y_init = 2

    @property
    def movements(self):
        if self.y == self.y_init:
            return {(0, 1), (0, 2)} | self.capture_movements
        return {(0, 1)} | self.capture_movements


class BlackPawn(Pawn):
    capture_movements = {(1, -1), (-1, -1)}
    y_init = 7

    @property
    def movements(self):
        if self.y == self.y_init:
            return {(0, -1), (0, -2)} | self.capture_movements
        return {(0, -1)} | self.capture_movements
