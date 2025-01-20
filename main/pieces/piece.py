from functools import cached_property
from typing import TYPE_CHECKING, Iterable, Optional, Reversible, Set

from main import constants
from main.game_tree import HalfMove
from main.types import Change, GameResult, LookaheadResults, Position
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
    fen_symbol: str = NotImplemented
    value: int = NotImplemented
    unicode: str = NotImplemented

    @cached_property
    def opponent(self) -> "Agent":
        attr = "black" if self.agent is self.agent.board.white else "white"
        return getattr(self.agent.board, attr)

    @property
    def position(self) -> Position:
        return self.x, self.y

    @property
    def forbidden_squares(self) -> Set[Position]:
        return self.agent.pieces_2

    @cached_property
    def king(self) -> "King":
        return self.agent.king

    def get_candidate_moves(self) -> Set[Position]:
        candidate_moves = set(
            (self.x + x_d, self.y + y_d) for x_d, y_d in self.movements
        )
        return candidate_moves & constants.SQUARES

    def is_valid_vector(self, new_position: Position) -> bool:
        raise NotImplementedError

    def is_valid_movement(self, new_position: Position) -> bool:
        if new_position in self.forbidden_squares:
            return False
        elif not self.is_valid_vector(new_position):
            return False
        return True

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

    def is_valid_move(self, new_position: Position) -> bool:
        if not self.is_valid_movement(new_position):
            return False
        elif not self.is_open_path(new_position):
            return False
        elif self.king_would_be_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        return True

    def get_valid_moves(self, lazy: Optional[bool] = False) -> Set[Position]:
        valid_moves = set()

        for cand in self.get_candidate_moves():
            # TODO? We're redundantly checking vectors here, but it doesn't seem to add much
            if self.is_valid_move(cand):
                valid_moves.add(cand)
                if lazy:
                    return valid_moves

        return valid_moves

    def can_move(self) -> Set[Position]:
        return self.get_valid_moves(lazy=True)

    def get_disambiguation(self, x: XPosition | str, y: int) -> str:
        """
        Used for algebraic notation. If we have other pieces of the same type
        that can also move to the target square, return the rank (y) and/or
        file (x) of this piece.
        e.g. 'h', '4', 'h4'
        """

        disambiguation = ""
        x = XPosition(x)
        siblings = [
            piece
            for piece in self.agent.pieces_2.values()
            if piece is not self and isinstance(piece, type(self))
        ]

        for sibling in siblings:
            if disambiguation in (f"{self.x}{self.y}", f"{self.y}{self.x}"):
                break
            if sibling.is_valid_move((x, y)):
                if sibling.x == self.x:
                    disambiguation += str(self.y)
                else:
                    # Sibling is on the same rank, or a different rank and file entirely,
                    # in which case we still prefer to disambiguate with the file
                    disambiguation += self.x

        # Remove duplicate characters, then sort them (e.g. 3c -> c3)
        return "".join(sorted(set(disambiguation), reverse=True))

    def king_would_be_in_check(
        self,
        king: "King",
        new_position: Optional[Position] = None,
        change: Optional[Change] = None,
    ) -> bool:
        # If we're constructing a new change, it means we're verifying King
        # safety for this Agent. Skip augmentations in this case - they can't
        # affect safety of my own king for this move, which is all we care
        # about here. Otherwise, this method will infinitely recurse.
        change = change or self.construct_change(*new_position, augment=False)

        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)
        in_check = king.is_in_check()
        self.agent.board.rollback_halfmove(halfmove)

        return in_check

    def get_game_result(self, check: bool, fen: str) -> GameResult:
        if check and not self.opponent.can_move():
            return "1-0" if self.agent.color == constants.WHITE else "0-1"
        elif (
            # .can_move() is computationally expensive; stalemate is
            # likely impossible until move 10, and in practice won't be
            # reached until much later than that (15+)
            # https://en.wikipedia.org/wiki/List_of_world_records_in_chess#:~:text=The%20shortest%20known%20stalemate%2C%20composed,Qh5%20Ra6%203.
            # 1.e3 a5 2.Qh5 Ra6 3.Qxa5 h5 4.Qxc7 Rah6 5.h4 f6 6.Qxd7+ Kf7
            # 7.Qxb7 Qd3 8.Qxb8 Qh7 9.Qxc8 Kg6 10.Qe6 ½-½
            self.agent.board.fullmove_number >= 10
            and not self.opponent.can_move()
        ):
            return "½-½ Stalemate"
        elif (
            # Safe guess...probably not possible to capture 28 pieces in 20 moves?
            self.agent.board.fullmove_number >= 20
            and self.agent.board.has_insufficient_material()
        ):
            return "½-½ Insufficient material"
        elif self.agent.board.draw_by_repetition(fen):
            return "½-½ Repetition"
        elif self.agent.board.halfmove_clock == 125:
            return "½-½ Seventy-five-move rule"
        return None

    def get_lookahead_results(self, change: Change) -> LookaheadResults:
        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)

        check = self.opponent.king.is_in_check()
        fen = self.agent.board.get_fen(internal=True)
        game_result = self.get_game_result(check=check, fen=fen)

        self.agent.board.rollback_halfmove(halfmove)

        return {"check": check, "fen": fen, "game_result": game_result}

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
            "halfmove_clock": (
                self.agent.board.halfmove_clock,
                self.agent.board.halfmove_clock + 1,
            ),
            "fullmove_number": (
                self.agent.board.fullmove_number,
                self.agent.board.fullmove_number
                + (1 if self.agent.color == constants.BLACK else 0),
            ),
        }

        if (x, y) in self.opponent.pieces_2:  # capture
            piece = self.opponent.get_by_position(x, y)
            change[self.opponent.color] = {
                piece.attr: {
                    "old_position": (x, y),
                    "new_position": None,
                }
            }
            change["halfmove_clock"] = (self.agent.board.halfmove_clock, 0)

        if augment:
            change = self.augment_change(x, y, change, **kwargs)
            change["disambiguation"] = self.get_disambiguation(x, y)

            if self.opponent.en_passant_target:
                change[self.opponent.color]["en_passant_target"] = (
                    self.opponent.en_passant_target,
                    None,
                )

            # These must be computed after the piece-specific augmentations in
            # augment_change because castling and promotion create new possibilities
            change = change | self.get_lookahead_results(change=change)

        return change

    def move(self, x: XPosition, y: int, **kwargs) -> HalfMove:
        change = self.construct_change(x, y, **kwargs)
        halfmove = HalfMove(color=self.agent.color, change=change)
        self.agent.board.apply_halfmove(halfmove)

        return halfmove
