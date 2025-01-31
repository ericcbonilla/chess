import pytest

from main.exceptions import BuildError, GameplayError
from main.pieces import King, Queen, WhitePawn
from main.x import A, B, C, D, E, F, G, H


class TestBoardBuilder:
    def test_no_king_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_data=[
                    {"piece_type": WhitePawn, "x": A, "y": 2},
                ],
                black_data=[
                    {"piece_type": King, "x": E, "y": 5},
                ],
            )

    def test_pawn_added_to_correct_slot(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": F, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
            ],
        )

        assert board.white.f_pawn

    def test_multiple_pawns_on_same_file_added_to_correct_slots(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": G, "y": 2},
                {"piece_type": WhitePawn, "x": G, "y": 3},
                {"piece_type": WhitePawn, "x": G, "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
            ],
        )

        assert board.white.g_pawn.position == (G, 2)
        assert board.white.h_pawn.position == (G, 3)
        assert board.white.a_pawn.position == (G, 4)

    def test_too_many_pawns_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_data=[
                    {"piece_type": King, "x": E, "y": 1},
                    {"piece_type": WhitePawn, "x": A, "y": 2},
                    {"piece_type": WhitePawn, "x": B, "y": 2},
                    {"piece_type": WhitePawn, "x": C, "y": 2},
                    {"piece_type": WhitePawn, "x": D, "y": 2},
                    {"piece_type": WhitePawn, "x": E, "y": 2},
                    {"piece_type": WhitePawn, "x": F, "y": 2},
                    {"piece_type": WhitePawn, "x": G, "y": 2},
                    {"piece_type": WhitePawn, "x": H, "y": 2},
                    {"piece_type": WhitePawn, "x": A, "y": 3},
                ],
                black_data=[
                    {"piece_type": King, "x": E, "y": 5},
                ],
            )

    def test_pawn_on_back_rank_raises_build_error(self, builder):
        with pytest.raises(BuildError):
            builder.from_data(
                white_data=[
                    {"piece_type": King, "x": E, "y": 1},
                    {"piece_type": WhitePawn, "x": A, "y": 1},
                ],
                black_data=[
                    {"piece_type": King, "x": E, "y": 5},
                ],
            )

    def test_second_added_queen_has_correct_name(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": Queen, "x": G, "y": 5},
                {"piece_type": Queen, "x": G, "y": 4},
                {"piece_type": Queen, "x": G, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
            ],
        )

        assert board.white.queen.position == (G, 5)
        assert board.white.g_prom.position == (G, 4)
        assert board.white.h_prom.position == (G, 3)

    def test_from_fen_starting_position_returns_expected_board(self, builder):
        board = builder.from_fen(
            text="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        )

        assert board.active_color == "w"
        assert not board.white.king.has_moved
        assert not board.white.a_rook.has_moved
        assert not board.white.h_rook.has_moved
        assert not board.black.king.has_moved
        assert not board.black.a_rook.has_moved
        assert not board.black.h_rook.has_moved
        assert board.get_fen(internal=True) == (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def test_from_fen_midgame_returns_expected_board(self, builder):
        board = builder.from_fen(
            text="rnb1k2r/1p1pnpp1/p1p4p/8/3BP3/1PNB1QP1/P1P2P1K/R4R2 w - - 0 14",
        )

        assert board.white.queen.position == (F, 3)
        assert board.black.king.has_moved

        with pytest.raises(GameplayError):
            board.black.move("a_pawn", A, 5)

        board.white.move("c_bishop", G, 7)

        assert board.get_fen(internal=True) == (
            "rnb1k2r/1p1pnpB1/p1p4p/8/4P3/1PNB1QP1/P1P2P1K/R4R2 b - - 0 14"
        )

    def test_from_fen_endgame_returns_expected_board(self, builder):
        board = builder.from_fen(
            text="6k1/3R4/5Q2/8/p3N3/1P4P1/P1P2P1K/8 w - - 0 39",
        )

        board.white.move("queen", D, 8)

        assert board.result == "1-0"
        assert (
            board.get_fen(internal=True)
            == "3Q2k1/3R4/8/8/p3N3/1P4P1/P1P2P1K/8 b - - 1 39"
        )

    def test_from_fen_correct_en_passant_target_is_set(self, builder):
        board = builder.from_fen(
            text="rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1",
        )

        assert board.white.en_passant_target == (D, 3)
