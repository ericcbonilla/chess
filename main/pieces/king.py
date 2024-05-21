from typing import TYPE_CHECKING, Optional, Set, Tuple

from main import constants
from main.game_tree import HalfMove
from main.types import Change, Position
from main.xposition import XPosition

from .knight import Knight
from .pawn import BlackPawn, WhitePawn
from .piece import Piece
from .rook import Rook

if TYPE_CHECKING:
    from main.agents import Agent


class King(Piece):
    movements = {(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)}
    capture_movements = movements
    symbol = "K"
    value = 0
    unicode = "\u2654"

    def __init__(
        self,
        attr: str,
        agent: "Agent",
        x: str,
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(attr, agent, x, y)

        if has_moved is None:
            initial_y = 1 if self.agent.color == constants.WHITE else 8
            self.has_moved = self.position != ("e", initial_y)
        else:
            self.has_moved = has_moved

    def _can_castle(self, rook: Rook | None) -> Tuple[str | None, bool]:
        if rook is None or rook.has_moved or self.has_moved or self.is_in_check():
            return None, False

        if rook.x == "a":  # Queenside
            castle_through_check = self.is_in_check(("d", self.y))
            new_king_xpos = "c"
        else:  # Kingside
            castle_through_check = self.is_in_check(("f", self.y))
            new_king_xpos = "g"

        return new_king_xpos, (
            not castle_through_check and self.is_open_path(rook.position)
        )

    def is_valid_move(
        self, new_position: Position, keep_king_safe: Optional[bool] = True
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.forbidden_squares
            or self.is_in_check(new_position)
        ):
            return False

        return True

    def get_valid_moves(self, lazy: Optional[bool] = False) -> Set[Position]:
        valid_moves = set()

        for x_d, y_d in self.movements:
            new_position = self.x + x_d, self.y + y_d
            if not self.is_valid_move(new_position):
                continue

            valid_moves.add(new_position)
            if lazy:
                return valid_moves

        for rook in (self.agent.a_rook, self.agent.h_rook):
            new_king_xpos, can_castle = self._can_castle(rook)
            if can_castle and new_king_xpos:
                valid_moves.add((new_king_xpos, self.y))

        return valid_moves

    def is_in_check(self, target_position: Optional[Position] = None) -> bool:
        """
        This is used in several different ways:
        1. To ensure a move from this King's agent would not leave this King in check
        (direct checks, pins)
        2. By the opponent agent to see if they've checked this King
        (direct checks, discoveries)
        3. To prevent castling out of check
        4. To prevent castling through check
        5. To prevent this King from moving into check

        1, 2, and 3 evaluate King safety based on its current position.

        4 and 5 evaluate based on a new, target position. For this we must apply
        and rollback the target move so that King safety is evaluated using that
        future King position. Otherwise, we allow for Kings to illegally move
        'backwards' when skewered, because is_open_path interprets the King as being
        'blocked' by itself.
        """

        if target_position:
            change = self.construct_change(*target_position, augment=False)
            halfmove = HalfMove(color=self.agent.color, change=change)

            self.agent.board.apply_halfmove(halfmove)
            is_capturable = self._is_capturable()
            self.agent.board.rollback_halfmove(halfmove)
        else:
            is_capturable = self._is_capturable()

        return is_capturable

    def _is_capturable(self) -> bool:
        # TODO: Think of a way to ~avoid~ calling this for every single move
        # Or at least try to reduce the number of opponent pieces that we evaluate
        # Maybe only loop over movable pieces? Maybe there's some piece of this
        # we could memoize?

        for _, piece in self.opponent.pieces:
            if isinstance(piece, (WhitePawn, BlackPawn, Knight, King)):
                for x_d, y_d in piece.capture_movements:
                    new_position = piece.x + x_d, piece.y + y_d
                    if new_position == self.position:
                        return True
            else:
                for x_d, y_d in piece.movements:
                    new_position = piece.x + x_d, piece.y + y_d
                    if new_position == self.position:
                        # Don't need to do a full validity check here, since most
                        # of those checks either don't apply or are redundant
                        if piece.is_open_path(new_position):
                            return True

        return False

    def get_disambiguation(self, x: XPosition, y: int) -> str:
        return ""

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        if not self.has_moved:
            change[self.agent.color][self.attr]["has_moved"] = True

            if (x, y) == ("c", self.y):  # queenside
                change[self.agent.color]["a_rook"] = {
                    "old_position": ("a", self.y),
                    "new_position": ("d", self.y),
                    "has_moved": True,
                }
            elif (x, y) == ("g", self.y):  # kingside
                change[self.agent.color]["h_rook"] = {
                    "old_position": ("h", self.y),
                    "new_position": ("f", self.y),
                    "has_moved": True,
                }

        return change
