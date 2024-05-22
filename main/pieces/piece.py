from typing import TYPE_CHECKING, Iterable, Optional, Reversible, Set

from colorist import red

from main import constants
from main.exceptions import InvalidMoveError
from main.game_tree import HalfMove
from main.types import Change, GameResult, Position
from main.utils import cprint
from main.xposition import XPosition

if TYPE_CHECKING:
    from main.agents import Agent
    from main.pieces import King


class Piece:
    """
    Responsibilities:
    - Compute my legal moves
    - Compute King safety
    - Move where I'm told by my agent (agnostic of strategy)
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({self.unicode}): {self.position}>"

    def __init__(self, attr: str, agent: "Agent", x: str, y: int):
        self.attr = attr
        self.agent = agent
        self.x = XPosition(x)
        self.y = y

    movements: Set = NotImplemented
    symbol: str = NotImplemented
    value: int = NotImplemented
    unicode: str = NotImplemented

    @property
    def opponent(self) -> "Agent":
        attr = "black" if self.agent is self.agent.board.white else "white"
        return getattr(self.agent.board, attr)

    @property
    def position(self) -> Position:
        return self.x, self.y

    @property
    def forbidden_squares(self) -> Set[Position]:
        return self.agent.positions

    @property
    def king(self) -> "King":
        return self.agent.king

    @staticmethod
    def _get_squares_in_range(old: int, new: int) -> Iterable | Reversible:
        if old > new:
            return range(*sorted((old, new)))[1:]
        else:
            return [p + 1 for p in range(*sorted((old, new)))][0:-1]

    def is_open_path(self, target_position: Position) -> bool:
        target_x, target_y = target_position
        x_range = self._get_squares_in_range(ord(self.x), ord(target_x))
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

        if squares_on_path & (self.agent.positions | self.opponent.positions):
            return False
        return True

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.forbidden_squares
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

    def can_move(self) -> Set[Position]:
        return self.get_valid_moves(lazy=True)

    def get_captures(
        self, valid_moves: Optional[Set[Position]] = None
    ) -> Set[Position]:
        valid_moves = valid_moves or set()
        return valid_moves & self.opponent.positions

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
            for _, piece in self.agent.pieces
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
        # safety for this Agent. Skip augmentations in this case - they can't
        # affect safety of my own king for this move, which is all we care
        # about here. Without this, it'll recursively call this method infinitely.
        change = change or self.construct_change(*new_position, augment=False)

        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)
        in_check = king.is_in_check()
        self.agent.board.rollback_halfmove(halfmove)

        return in_check

    def get_game_result(self, change: Change) -> GameResult:
        # TODO start here decide where to update halfmove_clock
        # We will need to update halfmove_clock and fullmove_number
        # the same way we update en_passant_target

        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)

        opponent_can_move = self.opponent.can_move()
        insufficient_material = self.agent.board.has_insufficient_material()
        halfmove_clock = self.agent.board.halfmove_clock

        self.agent.board.rollback_halfmove(halfmove)

        if change["check"] and not opponent_can_move:
            return "1-0" if self.agent.color == constants.WHITE else "0-1"
        elif not opponent_can_move:
            return "½-½ Stalemate"
        elif insufficient_material:
            return "½-½ Insufficient material"
        elif halfmove_clock == 125:
            return "½-½ Seventy-five-move rule"
        return None

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
        change = {
            self.agent.color: {
                self.attr: {
                    "old_position": (self.x, self.y),
                    "new_position": (x, y),
                }
            },
            self.opponent.color: {},
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": self.symbol,
        }

        if (x, y) in self.opponent.positions:  # capture
            piece = self.opponent.get_by_position(x, y)
            change[self.opponent.color] = {
                piece.attr: {
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
                king=self.opponent.king,
                change=change,
            )
            change["game_result"] = self.get_game_result(change=change)

            if self.opponent.en_passant_target:
                change[self.opponent.color]["en_passant_target"] = (
                    self.opponent.en_passant_target,
                    None,
                )

        return change

    def move(self, x: XPosition, y: int, **kwargs) -> Change:
        change = self.construct_change(x, y, **kwargs)
        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)

        return change

    # TODO manual_move should be part of ManualAgent
    def manual_move(self, x: str, y: int, **kwargs) -> Change:
        x = XPosition(x)
        valid_moves = self.get_valid_moves()
        captures = self.get_captures(valid_moves)

        if (x, y) in captures:
            cprint(self.agent.color, f"{self} capturing on {(x, y)}", color_fn=red)
            return self.move(x, y, **kwargs)
        elif (x, y) in valid_moves:
            cprint(self.agent.color, f"Moving {self} to {(x, y)}")
            return self.move(x, y, **kwargs)

        raise InvalidMoveError(f"Moving {self} to {(x, y)} is invalid")
