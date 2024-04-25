from typing import Set, Union, Type, Dict, Optional

from main import constants
from main.exceptions import PromotionError
from main.types import Position, Change
from main.xposition import XPosition
from .piece import Piece
from .bishop import Bishop
from .knight import Knight
from .rook import Rook
from .queen import Queen


class Pawn(Piece):
    symbol = ''
    value = 1
    capture_movements: Set = NotImplemented
    unicode = '\u2659'

    def is_valid_move(
        self,
        new_position: Position,
        keep_king_safe: Optional[bool] = True,
    ) -> bool:
        if (
            new_position not in constants.SQUARES
            or new_position in self.team.positions | self.opponent_team.positions
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

        if new_position == self.opponent_team.en_passant_target:
            return True

        return new_position in self.opponent_team.positions

    def can_move(self):
        return self.get_valid_moves(lazy=True) or self.get_captures()

    def get_captures(self, valid_moves: Optional[Set[Position]] = None) -> Set[Position]:
        # Arg valid_moves isn't used here, because pawns are the only pieces
        # whose captures are not a subset of their valid moves
        captures = set()

        for x_d, y_d in self.capture_movements:
            move = self.x + x_d, self.y + y_d

            if self.is_valid_capture(move):
                captures.add(move)

        return captures

    @staticmethod
    def _get_promotion_piece_type(promotion_type: str) -> Type[Union[Bishop, Knight, Rook, Queen]]:
        if promotion_type == 'B':
            return Bishop
        elif promotion_type == 'N':
            return Knight
        elif promotion_type == 'R':
            return Rook
        elif promotion_type == 'Q':
            return Queen
        else:
            raise PromotionError('Invalid promotion_type, must be one of B, N, R, or Q')

    def get_disambiguation(self, x: Union[XPosition, str], y: int) -> str:
        """
        Algebraic notation disambiguates pawns by default
        """

        return ''

    def augment_change(self, x: Union[XPosition, str], y: int, change: Change, **kwargs) -> Change:
        if (x, y) == self.opponent_team.en_passant_target:
            piece = self.opponent_team.get_by_position(x, self.y)
            change[self.opponent_team.color] = {
                piece.name: {
                    'old_position': (x, self.y),
                    'new_position': None,
                }
            }

        if not self.is_promotion(y):
            return change
        elif 'promotion_type' not in kwargs:
            # If king_is_in_check is testing a promotion move, we must provide a piece type.
            # Just assume Queen in this case
            promotion_type = 'Q'
        else:
            # Let's also assume that whatever client is sending the move knows
            # when it needs to supply a promotion_type
            promotion_type = kwargs['promotion_type']

        promotion_piece_type = self._get_promotion_piece_type(promotion_type)
        promotion_piece_name = self.board.get_piece_name(
            piece_type=promotion_piece_type,
            color=self.team.color,
        )

        change[self.team.color][self.name]['new_position'] = None
        change[self.team.color][promotion_piece_name] = {
            'old_position': None,
            'new_position': (x, y),
            'piece_type': promotion_piece_type,
        }

        return change

    def move(self, x: Union[XPosition, str], y: int, **kwargs) -> Dict:
        if abs(self.y - y) == 2:
            target_y = int((self.y + y) / 2)
            self.team.en_passant_target = (self.x, target_y)

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
