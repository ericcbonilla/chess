from typing import Callable, Optional

from colorist import bright_red

from main.exceptions import GameplayError, InvalidMoveError, NotationError
from main.game_tree import HalfMove
from main.notation import AN
from main.pieces import King, Pawn, Piece
from main.types import Position, X
from main.x import to_str

from .agent import Agent


class ManualAgent(Agent):
    @staticmethod
    def _get_disamb_search_fn(an: AN) -> Callable[[Piece], bool]:
        if isinstance(an.disambiguation, X):
            return lambda p: p.x == an.disambiguation
        elif isinstance(an.disambiguation, int):
            return lambda p: p.y == an.disambiguation
        else:
            return lambda p: p.position == an.disambiguation

    def _get_matching_piece(self, an: AN, pick: Position) -> Piece:
        search_fn: Callable[[Piece], bool] = lambda p: True
        piece = None

        if an.piece_type is King:
            piece = self.king
        elif an.piece_type is Pawn:
            search_fn: Callable[[Piece], bool] = lambda p: (
                p.x == an.pawn_file if an.is_capture else an.x
            )
        elif an.disambiguation:
            search_fn = self._get_disamb_search_fn(an=an)

        if piece is None:
            pieces = list(self.pieces.values())
            matching_pieces = [
                piece
                for piece in pieces
                if (
                    search_fn(piece)
                    and isinstance(piece, an.piece_type)
                    and piece.is_valid_move(pick)
                )
            ]

            if len(matching_pieces) > 1:
                raise NotationError(
                    f"More than one {an.piece_type.__name__} can move to {to_str(an.x)}{an.y};"
                    f" disambiguation required"
                )
            try:
                piece = matching_pieces.pop()
            except IndexError:
                raise NotationError(f'"{an.text}" is an illegal move')
        else:
            if not piece.is_valid_move(pick):
                raise NotationError(f'"{an.text}" is an illegal move')

        if not an.is_capture and an.pick in piece.opponent.pieces:
            raise NotationError(
                f"Opponent piece on {to_str(an.x)}{an.y}. "
                f"Did you mean {piece.symbol}x{an.text[1:]}?"
            )
        elif an.is_capture and an.pick not in piece.opponent.pieces:
            raise NotationError(
                f"No opponent piece on {an.x}{an.y}. "
                f"Did you mean {piece.symbol}{an.x}{an.y}?"
            )

        return piece

    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[X] = None,
        y: Optional[int] = None,
        an_text: Optional[str] = None,
        **kwargs,
    ) -> Optional[HalfMove]:
        if self is not self.board.active_agent:
            raise GameplayError("Agent is not active")
        elif self.board.result:
            raise GameplayError("The game has ended")

        if attr and x and y:
            piece = getattr(self, attr)

            if piece.is_valid_move((x, y)):
                return piece.move(x, y, **kwargs)

            raise InvalidMoveError(f"Moving {piece} to {(x, y)} is invalid")
        else:
            an, pick, piece = None, None, None
            while piece is None:
                try:
                    text = an_text or input(f"Enter move for {self.color}: ")
                    an = AN(text=text)
                    pick = an.pick or (an.x, self.king.y)
                    piece = self._get_matching_piece(an, pick)
                except NotationError as e:
                    bright_red(str(e))
                    if an_text:
                        an_text = None

            kwargs = kwargs or {}
            if an.promotee_type:
                kwargs = {"promotee_type": an.promotee_type}

            return piece.move(*pick, **kwargs)
