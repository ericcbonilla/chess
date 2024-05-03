import pytest

from main.board import Board
from main.exceptions import InvalidMoveError
from main.pieces import King, Rook


class TestRookScenarios:
    def test_cant_castle_if_rook_has_moved(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, agent=board.black, x="e", y=8),
                Rook(board=board, agent=board.black, x="a", y=8),
                Rook(board=board, agent=board.black, x="h", y=8),
                King(board=board, agent=board.white, x="e", y=1),
            ]
        )

        board.black["R2"].manual_move("h", 7)
        board.black["R2"].manual_move("h", 8)

        with pytest.raises(InvalidMoveError):
            board.black["K"].manual_move("g", 8)

    def test_castle_with_only_one_rook_on_board(self):
        """
        If a kingside castle is valid but we were never given a queenside rook,
        we check for R1 instead of R2 (pieces should be added left to right)
        """

        board = Board()
        board.add_pieces(
            [
                King(board=board, agent=board.black, x="e", y=8),
                Rook(board=board, agent=board.black, x="h", y=8),
                King(board=board, agent=board.white, x="e", y=1),
            ]
        )

        board.black["K"].manual_move("g", 8)

        assert board.black["K"].position == ("g", 8)
        assert board.black["R1"].position == ("f", 8)
