from typing import Optional, Set, Type

from main import constants
from main.exceptions import PromotionError
from main.types import Change, Position, Promotee
from main.xposition import XPosition

from .bishop import Bishop
from .knight import Knight
from .piece import Piece
from .queen import Queen
from .rook import Rook


class Pawn(Piece):
    symbol = ""
    value = 1
    capture_movements: Set = NotImplemented
    unicode = "\u2659"

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.agent.positions | self.opponent_agent.positions
            or not self.is_open_path(new_position)
        ):
            return False
        elif keep_king_safe and self.king_is_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        return True

    def is_valid_capture(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if keep_king_safe and self.king_is_in_check(
            king=self.king,
            new_position=new_position,
        ):
            return False

        if new_position == self.opponent_agent.en_passant_target:
            return True

        return new_position in self.opponent_agent.positions

    def can_move(self) -> Set[Position]:
        return self.get_valid_moves(lazy=True) or self.get_captures()

    def get_captures(
        self, valid_moves: Optional[Set[Position]] = None
    ) -> Set[Position]:
        # Arg valid_moves isn't used here, because pawns are the only pieces
        # whose captures are not a subset of their valid moves
        captures = set()

        for x_d, y_d in self.capture_movements:
            move = self.x + x_d, self.y + y_d

            if self.is_valid_capture(move):
                captures.add(move)

        return captures

    @staticmethod
    def get_promotee_type(
        promotee_value: str,
    ) -> Type[Promotee]:
        if promotee_value == "B":
            return Bishop
        elif promotee_value == "N":
            return Knight
        elif promotee_value == "R":
            return Rook
        elif promotee_value == "Q":
            return Queen
        else:
            raise PromotionError("Invalid promotee value, must be one of B, N, R, or Q")

    def get_disambiguation(self, x: XPosition, y: int) -> str:
        """
        Algebraic notation disambiguates pawns by default
        """

        return ""

    def augment_change(self, x: XPosition, y: int, change: Change, **kwargs) -> Change:
        if (x, y) == self.opponent_agent.en_passant_target:
            piece = self.opponent_agent.get_by_position(x, self.y)
            change[self.opponent_agent.color] = {
                piece.attr: {
                    "old_position": (x, self.y),
                    "new_position": None,
                }
            }

        if not self.is_promotion(y):
            return change

        if "promotee_value" not in kwargs:
            # If king_is_in_check is testing a promotion move, we must provide a piece type.
            # Just assume Queen in this case. Or, if a promotee_value is not provided,
            # also just assume Queen. You could play a decade of chess and never find a
            # situation where you need a Knight. This is fine for our purposes.
            promotee_value = "Q"
        else:
            # Let's also assume that whatever client is sending the move knows
            # when it needs to supply a promotee_value
            promotee_value = kwargs["promotee_value"]

        promotion_piece_type = self.get_promotee_type(promotee_value)
        change[self.agent.color][self.attr]["new_position"] = None
        change[self.agent.color][f"{self.attr[0]}_prom"] = {
            "old_position": None,
            "new_position": (x, y),
            "piece_type": promotion_piece_type,
        }

        return change

    def move(self, x: XPosition, y: int, **kwargs) -> Change:
        if abs(self.y - y) == 2:
            target_y = int((self.y + y) / 2)
            self.agent.en_passant_target = (self.x, target_y)

        return super().move(x, y, **kwargs)

    @staticmethod
    def is_promotion(y: int) -> bool:
        return y in (1, 8)


class WhitePawn(Pawn):
    capture_movements = {(1, 1), (-1, 1)}

    @property
    def movements(self):
        if self.y == 2:
            return {(0, 1), (0, 2)}
        return {(0, 1)}


class BlackPawn(Pawn):
    capture_movements = {(1, -1), (-1, -1)}

    @property
    def movements(self):
        if self.y == 7:
            return {(0, -1), (0, -2)}
        return {(0, -1)}
