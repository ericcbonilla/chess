from typing import Callable, Optional

from colorist import bright_red, red

from main.exceptions import InvalidMoveError, NotationError
from main.game_tree import HalfMove
from main.notation import AN
from main.pieces import King, Pawn, Piece
from main.types import Position
from main.utils import cprint
from main.xposition import XPosition

from .agent import Agent


class ManualAgent(Agent):
    def _get_matching_piece(self, an: AN, pick: Position) -> Piece:
        search_fn: Callable[[Piece], bool] = lambda p: True

        # TODO can we use similar logic to optimize get_valid_moves()?
        if an.piece_type is King:
            if pick in self.king.get_valid_moves():
                return self.king
            else:
                raise NotationError(f'"{an.text}" is an illegal move')
        elif an.piece_type is Pawn:
            if an.is_capture:
                search_fn: Callable[[Piece], bool] = lambda p: p.x == an.pawn_file
            else:
                search_fn: Callable[[Piece], bool] = lambda p: p.x == an.x

        matching_pieces = [
            piece
            for _, piece in self.pieces
            if (
                search_fn(piece)
                and isinstance(piece, an.piece_type)
                and (pick in piece.get_valid_moves() or pick in piece.get_captures())
            )
        ]

        if len(matching_pieces) > 1:
            raise NotationError(
                f"More than one {an.piece_type} can move to {an.x}{an.y};"
                f"disambiguation required"
            )
        try:
            piece = matching_pieces.pop()
        except IndexError:
            raise NotationError(f'"{an.text}" is an illegal move')

        # TODO these need to be applied to King moves as well
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
    ) -> Optional[HalfMove]:
        if attr and x and y:
            piece = getattr(self, attr)
            x = XPosition(x)
            valid_moves = piece.get_valid_moves()
            captures = piece.get_captures(valid_moves)

            if (x, y) in valid_moves | captures:
                return piece.move(x, y)

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

            if an.is_capture:
                cprint(self.color, f"{piece} capturing on {pick}", color_fn=red)
            else:
                cprint(self.color, f"Moving {piece} to {pick}")

            return piece.move(*pick)
