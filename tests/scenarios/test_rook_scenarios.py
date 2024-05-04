import pytest

from main.agents import ManualAgent
from main.exceptions import InvalidMoveError
from main.pieces import King, Rook


class TestRookScenarios:
    def test_when_rook_added_on_starting_square_has_moved_false(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "a", "y": 8},
                {"piece_type": Rook, "x": "h", "y": 8},
            ],
        )

        assert not board.black.a_rook.has_moved
        assert not board.black.h_rook.has_moved

    def test_when_rook_added_not_on_starting_square_has_moved_true(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "a", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 1},
            ],
        )

        assert board.black.a_rook.has_moved
        assert board.black.h_rook.has_moved

    def test_cant_castle_if_rook_has_moved(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "a", "y": 8},
                {"piece_type": Rook, "x": "h", "y": 8},
            ],
        )

        board.black.h_rook.manual_move("h", 7)
        board.black.h_rook.manual_move("h", 8)

        with pytest.raises(InvalidMoveError):
            board.black.king.manual_move("g", 8)

    def test_castle_with_only_one_rook_on_board(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "h", "y": 8},
            ],
        )

        board.black.king.manual_move("g", 8)

        assert board.black.king.position == ("g", 8)
        assert board.black.h_rook.position == ("f", 8)
