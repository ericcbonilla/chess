import pytest

from main.exceptions import InvalidMoveError
from main.pieces import BlackPawn, King, Knight, Queen, Rook, WhitePawn
from main.x import A, B, C, D, E, F, G, H


class TestPawnScenarios:
    def test_pawn_can_capture_pawn(self, default_board):
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("d_pawn", D, 5)

        default_board.white.move("e_pawn", D, 5)

        assert default_board.white.e_pawn.position == (D, 5)
        assert default_board.black.d_pawn is None
        assert default_board.black.graveyard.d_pawn

    def test_pawn_cannot_capture_forward(self, default_board):
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("e_pawn", E, 5)

        with pytest.raises(InvalidMoveError):
            default_board.white.move("e_pawn", E, 5)

    def test_pawn_cannot_capture_two_squares_forward(self, default_board):
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("a_pawn", A, 6)
        default_board.white.move("e_pawn", E, 5)

        with pytest.raises(InvalidMoveError):
            default_board.black.move("e_pawn", E, 5)

    def test_pawn_cannot_capture_backwards_diagonally(self, default_board):
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("d_pawn", D, 5)
        default_board.white.move("e_pawn", E, 5)
        default_board.black.move("d_pawn", D, 4)

        # Trying to capture backwards diagonally
        with pytest.raises(InvalidMoveError):
            default_board.white.move("e_pawn", D, 4)

    def test_pawn_promotion_capture_results_in_expected_state(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": F, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Rook, "x": G, "y": 8},
            ],
        )

        board.white.move("f_pawn", G, 8, promotee_type=Queen)

        assert board.white.graveyard.f_pawn
        assert board.black.graveyard.a_rook
        assert board.white.f_prom.position == (G, 8)

    def test_rollback_pawn_promotion_capture_results_in_expected_state(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": F, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Rook, "x": G, "y": 8},
            ],
        )

        board.white.move("f_pawn", G, 8, promotee_type=Queen)
        board.rollback_halfmove()

        assert board.white.f_pawn.position == (F, 7)
        assert board.black.a_rook.position == (G, 8)
        assert board.white.f_prom is None
        assert board.white.graveyard.f_prom

    def test_pawn_promotion_can_create_third_piece(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": A, "y": 7},
                {"piece_type": Knight, "x": A, "y": 1},
                {"piece_type": Knight, "x": B, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
            ],
        )

        board.white.move("a_pawn", A, 8, promotee_type=Knight)

        assert isinstance(board.white.a_prom, Knight)
        assert board.white.a_prom.position == (A, 8)

    def test_pawn_promotion_capture_results_in_expected_piece(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": F, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Rook, "x": G, "y": 8},
            ],
        )

        board.white.move("f_pawn", G, 8, promotee_type=Knight)

        assert isinstance(board.white.f_prom, Knight)
        assert board.white.f_prom.position == (G, 8)
        assert board.black.graveyard.a_rook

    def test_pawn_promotion_invalid_if_king_is_in_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": H, "y": 7},
                {"piece_type": WhitePawn, "x": F, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Queen, "x": A, "y": 7},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("f_pawn", F, 8, promotee_type=Queen)

        # Also check that the pawn is left unchanged - we want to ensure
        # the king_would_be_in_check method has no side effects
        assert board.white.f_pawn.position == (F, 7)
        assert board.white.queen is None

    def test_pawn_promotion_capture_results_in_expected_change(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": WhitePawn, "x": F, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Rook, "x": G, "y": 8},
            ],
        )
        halfmove = board.white.move("f_pawn", G, 8, promotee_type=Queen)

        assert halfmove.change == {
            "WHITE": {
                "f_pawn": {
                    "old_position": (F, 7),
                    "new_position": None,
                },
                "f_prom": {
                    "old_position": None,
                    "new_position": (G, 8),
                    "piece_type": Queen,
                },
            },
            "BLACK": {
                "a_rook": {
                    "old_position": (G, 8),
                    "new_position": None,
                }
            },
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": "",
            "halfmove_clock": (0, 0),
            "fullmove_number": (1, 1),
            "fen": "6Q1/8/8/4k3/2K5/8/8/8 b - - 0 1",
            "rows_changing": {8, 7},
        }


class TestEnPassant:
    def test_white_pawn_moving_two_squares_sets_en_passant_target(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": WhitePawn, "x": E, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
            ],
        )

        board.white.move("e_pawn", E, 4)

        assert board.white.en_passant_target == (E, 3)

    def test_black_pawn_moving_two_squares_sets_en_passant_target(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": BlackPawn, "x": D, "y": 7},
            ],
            active_color="b",
        )

        board.black.move("d_pawn", D, 5)

        assert board.black.en_passant_target == (D, 6)

    def test_pawn_moving_one_square_does_not_set_en_passant_target(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": WhitePawn, "x": E, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
            ],
        )

        board.white.move("e_pawn", E, 3)

        assert board.white.en_passant_target is None

    def test_pawn_cannot_capture_en_passant_if_target_has_expired(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("g_pawn", G, 6)
        default_board.white.move("d_pawn", D, 5)
        default_board.black.move("e_pawn", E, 5)

        assert default_board.black.en_passant_target == (E, 6)

        # Waiting move
        default_board.white.move("queen", D, 2)
        default_board.black.move("g_pawn", G, 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white.move("d_pawn", E, 6)

    def test_pawn_cannot_capture_en_passant_if_target_did_not_advance_two_squares(
        self, default_board
    ):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("g_pawn", G, 6)
        default_board.white.move("d_pawn", D, 5)
        default_board.black.move("e_pawn", E, 6)

        # Waiting move
        default_board.white.move("queen", D, 2)
        default_board.black.move("e_pawn", E, 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white.move("d_pawn", E, 6)

    def test_capturing_en_passant_results_in_expected_state(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("g_pawn", G, 6)
        default_board.white.move("d_pawn", D, 5)
        default_board.black.move("e_pawn", E, 5)

        # En passant
        halfmove = default_board.white.move("d_pawn", E, 6)

        assert default_board.white.d_pawn.position == (E, 6)
        assert default_board.black.graveyard.e_pawn
        assert default_board.black.en_passant_target is None
        assert halfmove.change == {
            "WHITE": {
                "d_pawn": {
                    "old_position": (D, 5),
                    "new_position": (E, 6),
                },
            },
            "BLACK": {
                "en_passant_target": ((E, 6), None),
                "e_pawn": {
                    "old_position": (E, 5),
                    "new_position": None,
                },
            },
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": "",
            "halfmove_clock": (0, 0),
            "fullmove_number": (3, 3),
            "fen": "rnbqkbnr/pppp1p1p/4P1p1/8/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 3",
            "rows_changing": {5, 6},
        }

    def test_rollback_en_passant_results_in_expected_state(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("g_pawn", G, 6)
        default_board.white.move("d_pawn", D, 5)
        default_board.black.move("e_pawn", E, 5)

        # En passant
        default_board.white.move("d_pawn", E, 6)
        default_board.rollback_halfmove()

        assert default_board.white.d_pawn.position == (D, 5)
        assert default_board.black.e_pawn.position == (E, 5)
        assert default_board.black.en_passant_target == (E, 6)
