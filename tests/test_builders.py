import pytest

from main.agents import ManualAgent
from main.exceptions import BuildError
from main.pieces import King, Queen, WhitePawn


class TestBoardBuilder:
    def test_no_king_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_agent_cls=ManualAgent,
                black_agent_cls=ManualAgent,
                white_data=[
                    {"piece_type": WhitePawn, "x": "a", "y": 2},
                ],
                black_data=[
                    {"piece_type": King, "x": "e", "y": 5},
                ],
            )

    def test_pawn_added_to_correct_slot(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        assert board.white.f_slot

    def test_multiple_pawns_on_same_file_added_to_correct_slots(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "g", "y": 2},
                {"piece_type": WhitePawn, "x": "g", "y": 3},
                {"piece_type": WhitePawn, "x": "g", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        assert board.white.g_slot.position == ("g", 2)
        assert board.white.h_slot.position == ("g", 3)
        assert board.white.a_slot.position == ("g", 4)

    def test_too_many_pawns_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_agent_cls=ManualAgent,
                black_agent_cls=ManualAgent,
                white_data=[
                    {"piece_type": King, "x": "e", "y": 1},
                    {"piece_type": WhitePawn, "x": "a", "y": 2},
                    {"piece_type": WhitePawn, "x": "b", "y": 2},
                    {"piece_type": WhitePawn, "x": "c", "y": 2},
                    {"piece_type": WhitePawn, "x": "d", "y": 2},
                    {"piece_type": WhitePawn, "x": "e", "y": 2},
                    {"piece_type": WhitePawn, "x": "f", "y": 2},
                    {"piece_type": WhitePawn, "x": "g", "y": 2},
                    {"piece_type": WhitePawn, "x": "h", "y": 2},
                    {"piece_type": WhitePawn, "x": "a", "y": 3},
                ],
                black_data=[
                    {"piece_type": King, "x": "e", "y": 5},
                ],
            )

    def test_pawn_on_back_rank_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_agent_cls=ManualAgent,
                black_agent_cls=ManualAgent,
                white_data=[
                    {"piece_type": King, "x": "e", "y": 1},
                    {"piece_type": WhitePawn, "x": "a", "y": 1},
                ],
                black_data=[
                    {"piece_type": King, "x": "e", "y": 5},
                ],
            )

    def test_second_added_queen_has_correct_name(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Queen, "x": "g", "y": 5},
                {"piece_type": Queen, "x": "g", "y": 4},
                {"piece_type": Queen, "x": "g", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        assert board.white.queen.position == ("g", 5)
        assert board.white.g_slot.position == ("g", 4)
        assert board.white.h_slot.position == ("g", 3)
