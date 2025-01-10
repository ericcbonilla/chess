from typing import Callable, Optional

from colorist import bright_red, red

from main.exceptions import GameplayError, InvalidMoveError, NotationError
from main.game_tree import HalfMove
from main.notation import AN
from main.pieces import King, Pawn, Piece
from main.types import Position
from main.utils import cprint
from main.xposition import XPosition

from .agent import Agent


class ManualAgent(Agent):
    @staticmethod
    def _get_disamb_search_fn(an: AN) -> Callable[[Piece], bool]:
        if isinstance(an.disambiguation, XPosition):
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
            matching_pieces = [
                piece
                for _, piece in self.pieces
                if (
                    search_fn(piece)
                    and isinstance(piece, an.piece_type)
                    and pick in piece.get_valid_moves()
                    or pick in piece.get_captures()
                )
            ]

            if len(matching_pieces) > 1:
                raise NotationError(
                    f"More than one {an.piece_type.__name__} can move to {an.x}{an.y};"
                    f" disambiguation required"
                )
            try:
                piece = matching_pieces.pop()
            except IndexError:
                raise NotationError(f'"{an.text}" is an illegal move')
        else:
            if pick not in piece.get_valid_moves():
                raise NotationError(f'"{an.text}" is an illegal move')

        if not an.is_capture and an.pick in piece.opponent.positions:
            raise NotationError(
                f"Opponent piece on {an.x}{an.y}. "
                f"Did you mean {piece.symbol}x{an.text[1:]}?"
            )
        elif an.is_capture and an.pick not in piece.opponent.positions:
            raise NotationError(
                f"No opponent piece on {an.x}{an.y}. "
                f"Did you mean {piece.symbol}{an.x}{an.y}?"
            )

        return piece

    def move(
        self,
        attr: Optional[str] = None,
        x: Optional[str | XPosition] = None,
        y: Optional[int] = None,
        an_text: Optional[str] = None,
        **kwargs,
    ) -> Optional[HalfMove]:
        if self is not self.board.active_agent:
            raise GameplayError("Agent is not active")

        if attr and x and y:
            piece = getattr(self, attr)
            x = XPosition(x)

            # TODO change this and get_matching_piece() to just call is_valid_move()
            # I think we're losing a lot of time calculating every valid move
            valid_moves = piece.get_valid_moves()
            captures = piece.get_captures(valid_moves)

            if (x, y) in valid_moves | captures:
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

            if an.is_capture:
                cprint(f"{piece} capturing on {pick}", self.color, color_fn=red)
            else:
                cprint(f"Moving {piece} to {pick}", self.color)

            return piece.move(*pick, **kwargs)
