import random
from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Reversible, Set

from colorist import red, white, yellow

from main import constants
from main.exceptions import InvalidMoveError
from main.game_tree import HalfMove
from main.types import Change, GameResult, Position
from main.xposition import XPosition

if TYPE_CHECKING:
    from main.board import Board
    from main.pieces import King
    from main.team import Team


class Piece:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({self.unicode}): {self.position}>"

    def __init__(self, board: "Board", team: "Team", x: str, y: int):
        self.board = board
        self.team = team
        self.x = XPosition(x)
        self.y = y
        self.name = ""

        if self.team.color == constants.WHITE:
            self.opponent_team: "Team" = self.board.black
        else:
            self.opponent_team: "Team" = self.board.white

    movements: Set = NotImplemented
    symbol: str = NotImplemented
    value: int = NotImplemented
    unicode: str = NotImplemented

    def _print(self, message: str, color: Optional[Callable] = None):
        color = color or (yellow if self.team.color == constants.BLACK else white)
        color(message)

    @property
    def position(self) -> Position:
        return self.x, self.y

    @property
    def king(self) -> "King":
        return self.team["K"]

    @staticmethod
    def _get_squares_in_range(old: int, new: int) -> Iterable | Reversible:
        if old > new:
            return range(*sorted((old, new)))[1:]
        else:
            return [p + 1 for p in range(*sorted((old, new)))][0:-1]

    def is_open_path(self, target_position: Position):
        target_x, target_y = target_position
        ord_x = ord(self.x)
        ord_target_x = ord(target_x)
        x_range = self._get_squares_in_range(ord_x, ord_target_x)
        y_range = self._get_squares_in_range(self.y, target_y)

        if self.x != target_x and self.y == target_y:  # Horizontal
            squares_on_path = {(chr(x), self.y) for x in x_range}
        elif self.x == target_x and self.y != target_y:  # Vertical
            squares_on_path = {(self.x, y) for y in y_range}
        else:  # Diagonal
            if target_x > self.x and target_y > self.y:  # NE
                pass
            elif target_x < self.x and target_y > self.y:  # NW
                x_range = reversed(x_range)
            elif target_x > self.x and target_y < self.y:  # SE
                y_range = reversed(y_range)
            else:  # SW
                x_range = reversed(x_range)
                y_range = reversed(y_range)
            squares_on_path = {(chr(x), y) for x, y in zip(x_range, y_range)}

        if squares_on_path & (self.team.positions | self.opponent_team.positions):
            return False
        return True

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.team.positions
            or not self.is_open_path(new_position)
        ):
            return False
        elif keep_king_safe and self.king_is_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        return True

    def get_valid_moves(self, lazy: Optional[bool] = False) -> Set[Position]:
        valid_moves = set()

        for x_d, y_d in self.movements:
            new_position = self.x + x_d, self.y + y_d

            if self.is_valid_move(new_position):
                valid_moves.add(new_position)
                if lazy:
                    return valid_moves

        return valid_moves

    def can_move(self):
        return self.get_valid_moves(lazy=True)

    def get_captures(
        self, valid_moves: Optional[Set[Position]] = None
    ) -> Set[Position]:
        valid_moves = valid_moves or set()
        return valid_moves & self.opponent_team.positions

    def get_disambiguation(self, x: XPosition, y: int) -> str:
        """
        Used for algebraic notation. If we have other pieces of the same type
        that can also move to the target square, return the rank (y) and/or
        file (x) of this piece.
        e.g. 'h', '4', 'h4'
        """

        disambiguation = ""
        siblings = [
            piece
            for piece in self.team.values()
            if piece is not self and isinstance(piece, type(self))
        ]

        for sibling in siblings:
            if disambiguation in (f"{self.x}{self.y}", f"{self.y}{self.x}"):
                break
            if (x, y) in sibling.get_valid_moves():
                if sibling.x == self.x:
                    disambiguation += str(self.y)
                else:
                    # Sibling is on the same rank, or a different rank and file entirely,
                    # in which case we still prefer to disambiguate with the file
                    disambiguation += self.x

        # Remove duplicate characters, then sort them (e.g. 3c -> c3)
        return "".join(sorted(set(disambiguation), reverse=True))

    def king_is_in_check(
        self,
        king: "King",
        new_position: Optional[Position] = None,
        change: Optional[Change] = None,
    ) -> bool:
        # If we're constructing a new change, it means we're verifying King
        # safety for this Team. Skip augmentations in this case - they can't
        # affect safety of my own king for this move, which is all we care
        # about here. Without this, it'll recursively call this method infinitely.
        change = change or self.construct_change(*new_position, augment=False)

        halfmove = HalfMove(color=self.team.color, change=change)
        self.board.apply_halfmove(halfmove)
        in_check = king.is_in_check()
        self.board.rollback_halfmove(halfmove)

        return in_check

    def get_game_result(self, change: Change) -> GameResult:
        halfmove = HalfMove(color=self.team.color, change=change)
        self.board.apply_halfmove(halfmove)
        opponent_can_move = self.opponent_team.can_move()
        self.board.rollback_halfmove(halfmove)

        if change["check"] and not opponent_can_move:
            return "1-0" if self.team.color == constants.WHITE else "0-1"
        elif not opponent_can_move:
            return "½-½"
        return ""

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        """
        Piece specific augmentations/side effects: castling, promotions, etc.
        """
        return change

    def construct_change(
        self,
        x: XPosition,
        y: int,
        augment: Optional[bool] = True,
        **kwargs,
    ) -> Change:
        # By this point we already know that the provided move is legal,
        # so we don't need to do any validation checks

        change = {
            self.team.color: {
                self.name: {
                    "old_position": (self.x, self.y),
                    "new_position": (x, y),
                }
            },
            self.opponent_team.color: {},
            "disambiguation": "",
            "check": False,
            "game_result": "",
        }

        if (x, y) in self.opponent_team.positions:  # capture
            piece = self.opponent_team.get_by_position(x, y)
            change[self.opponent_team.color] = {
                piece.name: {
                    "old_position": (x, y),
                    "new_position": None,
                }
            }

        if augment:
            change = self.augment_change(x, y, change, **kwargs)
            change["disambiguation"] = self.get_disambiguation(x, y)

            # These must be computed after the piece-specific augmentations in
            # augment_change because castling and promotion create new possibilities
            change["check"] = self.king_is_in_check(
                king=self.opponent_team["K"],
                change=change,
            )
            change["game_result"] = self.get_game_result(change=change)

            if self.opponent_team.en_passant_target:
                change[self.opponent_team.color]["en_passant_target"] = (
                    self.opponent_team.en_passant_target,
                    None,
                )

        return change

    def move(self, x: XPosition, y: int, **kwargs) -> Dict:
        change = self.construct_change(x, y, **kwargs)
        halfmove = HalfMove(color=self.team.color, change=change)
        self.board.apply_halfmove(halfmove)

        return change

    def random_move(self) -> Optional[Dict]:
        valid_moves = self.get_valid_moves()
        captures = self.get_captures(valid_moves)
        legal_moves = list(valid_moves | captures)

        if not legal_moves:
            return None

        pick = random.sample(legal_moves, 1)[0]
        if pick in self.opponent_team.positions | {
            self.opponent_team.en_passant_target
        }:
            self._print(f"{self} capturing on {pick}", color=red)
        else:
            self._print(f"Moving {self} to {pick}")

        return self.move(*pick)

    def manual_move(self, x: str, y: int, **kwargs) -> Dict:
        x = XPosition(x)
        valid_moves = self.get_valid_moves()
        captures = self.get_captures(valid_moves)

        if (x, y) in captures:
            self._print(f"{self} capturing on {(x, y)}", color=red)
            return self.move(x, y, **kwargs)
        elif (x, y) in valid_moves:
            self._print(f"Moving {self} to {(x, y)}")
            return self.move(x, y, **kwargs)

        raise InvalidMoveError(f"Moving {self} to {(x, y)} is invalid")
