from typing import TYPE_CHECKING, Optional, Set, Tuple

from main import constants
from main.game_tree import HalfMove
from main.pieces.utils import vector
from main.types import Change, Position, X
from main.x import A, C, D, E, F, G, H

from .knight import Knight
from .pawn import BlackPawn, WhitePawn
from .piece import Piece
from .rook import Rook

if TYPE_CHECKING:
    from main.agents import Agent


class King(Piece):
    movements = [
        [(1, 0)],
        [(0, 1)],
        [(-1, 0)],
        [(0, -1)],
        [(1, 1)],
        [(1, -1)],
        [(-1, 1)],
        [(-1, -1)],
    ]
    castle_movements = [(-2, 0), (2, 0)]
    symbol = "K"
    fen_symbol = symbol
    value = 0
    unicode = "\u2654"

    def __init__(
        self,
        attr: str,
        agent: "Agent",
        x: X,
        y: int,
        has_moved: Optional[bool] = None,
    ):
        super().__init__(attr, agent, x, y)

        if has_moved is None:
            initial_y = 1 if self.agent.color == constants.WHITE else 8
            self.has_moved = self.position != (E, initial_y)
        else:
            self.has_moved = has_moved

    def _can_castle(self, rook: Rook | None) -> Tuple[int | None, bool]:
        if (
            rook is None
            or rook.has_moved
            or self.has_moved
            or self.is_in_check()
            or not self.is_open_path((rook.x, rook.y))
        ):
            return None, False

        if rook.x == A:  # Queenside
            castle_through_check = self.is_in_check((D, self.y))
            castle_into_check = self.is_in_check((C, self.y))
            new_king_xpos = C
        else:  # Kingside
            castle_through_check = self.is_in_check((F, self.y))
            castle_into_check = self.is_in_check((G, self.y))
            new_king_xpos = G

        return new_king_xpos, (not castle_through_check and not castle_into_check)

    def is_castle(self, new_position: Position) -> bool:
        return any(
            (self.x + x_d, self.y + y_d) == new_position
            for x_d, y_d in self.castle_movements
        )

    def is_valid_vector(self, new_position: Position) -> bool:
        return vector((self.x, self.y), new_position) in {(1, 1), (0, 1), (1, 0)}

    def is_valid_move(self, new_position: Position) -> bool:
        new_x, _ = new_position
        if self.is_castle(new_position):
            if new_x == C:
                _, can_castle = self._can_castle(self.agent.a_rook)
                return can_castle
            elif new_x == G:
                _, can_castle = self._can_castle(self.agent.h_rook)
                return can_castle
        elif not self.is_valid_movement(new_position) or self.is_in_check(new_position):
            return False

        return True

    def get_valid_moves(self, lazy: Optional[bool] = False) -> Set[Position]:
        valid_moves = super().get_valid_moves(lazy=lazy)

        if lazy and valid_moves:
            return valid_moves

        for rook in (self.agent.a_rook, self.agent.h_rook):
            new_king_xpos, can_castle = self._can_castle(rook)
            if can_castle and new_king_xpos:
                valid_moves.add((new_king_xpos, self.y))
                if lazy:
                    return valid_moves

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
        for piece in self.opponent.pieces.values():
            if isinstance(piece, (WhitePawn, BlackPawn)):
                skip = not piece.is_capture((self.x, self.y))
            else:
                skip = not piece.is_valid_vector((self.x, self.y))
            if skip:
                continue

            if isinstance(piece, (Knight, King)):
                return True
            elif isinstance(piece, (WhitePawn, BlackPawn)):
                if piece.is_capture((self.x, self.y)):
                    return True
            else:
                if piece.is_open_path((self.x, self.y)):
                    return True

        return False

    def get_disambiguation(self, x: X, y: int) -> str:
        return ""

    def augment_change(self, x: X, y: int, change: Change, **kwargs) -> Change:
        if not self.has_moved:
            change[self.agent.color][self.attr]["has_moved"] = True

            if (x, y) == (C, self.y):  # queenside
                change[self.agent.color]["a_rook"] = {
                    "old_position": (A, self.y),
                    "new_position": (D, self.y),
                    "has_moved": True,
                }
            elif (x, y) == (G, self.y):  # kingside
                change[self.agent.color]["h_rook"] = {
                    "old_position": (H, self.y),
                    "new_position": (F, self.y),
                    "has_moved": True,
                }

        return change
