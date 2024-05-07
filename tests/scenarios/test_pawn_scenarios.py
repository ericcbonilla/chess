import pytest

from main.agents import ManualAgent
from main.exceptions import InvalidMoveError
from main.pieces import BlackPawn, King, Knight, Queen, Rook, WhitePawn


class TestPawnScenarios:
    def test_pawn_can_capture_pawn(self, default_board):
        default_board.white.e_slot.manual_move("e", 4)
        default_board.black.d_slot.manual_move("d", 5)

        default_board.white.e_slot.manual_move("d", 5)

        assert default_board.white.e_slot.position == ("d", 5)
        assert default_board.black.d_slot is None
        assert default_board.black.graveyard.d_slot

    def test_pawn_cannot_capture_forward(self, default_board):
        default_board.white.e_slot.manual_move("e", 4)
        default_board.black.e_slot.manual_move("e", 5)

        with pytest.raises(InvalidMoveError):
            default_board.white.e_slot.manual_move("e", 5)

    def test_pawn_promotion_capture_results_in_expected_state(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Rook, "x": "g", "y": 8},
            ],
        )

        board.white.f_slot.manual_move("g", 8, promotee_value="Q")

        assert board.black.graveyard.a_rook

        assert board.white.graveyard.f_slot
        assert isinstance(board.white.graveyard.f_slot, WhitePawn)

        assert board.white.f_slot.position == ("g", 8)
        assert isinstance(board.white.f_slot, Queen)

    def test_rollback_pawn_promotion_capture_results_in_expected_state(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Rook, "x": "g", "y": 8},
            ],
        )

        board.white.f_slot.manual_move("g", 8, promotee_value="Q")

        board.rollback_halfmove()

        assert board.black.a_rook.position == ("g", 8)

        assert isinstance(board.white.f_slot, WhitePawn)
        assert board.white.f_slot.position == ("f", 7)

    def test_pawn_promotion_can_create_third_piece(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "a", "y": 7},
                {"piece_type": Knight, "x": "a", "y": 1},
                {"piece_type": Knight, "x": "b", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        board.white.a_slot.manual_move("a", 8, promotee_value="N")

        assert isinstance(board.white.a_slot, Knight)
        assert board.white.a_slot.position == ("a", 8)

    def test_pawn_promotion_capture_results_in_expected_piece(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Rook, "x": "g", "y": 8},
            ],
        )

        board.white.f_slot.manual_move("g", 8, promotee_value="N")

        assert isinstance(board.white.f_slot, Knight)
        assert board.white.f_slot.position == ("g", 8)
        assert board.black.graveyard.a_rook

    def test_pawn_promotion_invalid_if_king_is_in_check(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "h", "y": 7},
                {"piece_type": WhitePawn, "x": "f", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Queen, "x": "a", "y": 7},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.f_slot.manual_move("f", 8, promotee_value="Q")

        # Also check that the pawn is left unchanged - we want to ensure
        # the king_is_in_check method has no side effects
        assert isinstance(board.white.f_slot, WhitePawn)
        assert board.white.f_slot.position == ("f", 7)
        assert board.white.queen is None

    def test_pawn_promotion_capture_results_in_expected_change(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Rook, "x": "g", "y": 8},
            ],
        )

        board.white.f_slot.manual_move("g", 8, promotee_value="Q")

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change == {
            "WHITE": {
                "f_slot": {
                    "old_position": ("f", 7),
                    "new_position": ("g", 8),
                    "piece_type": Queen,
                },
            },
            "BLACK": {
                "a_rook": {
                    "old_position": ("g", 8),
                    "new_position": None,
                }
            },
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": "",
        }


class TestEnPassant:
    def test_white_pawn_moving_two_squares_sets_en_passant_target(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        board.white.e_slot.manual_move("e", 4)

        assert board.white.en_passant_target == ("e", 3)

    def test_black_pawn_moving_two_squares_sets_en_passant_target(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": BlackPawn, "x": "d", "y": 7},
            ],
        )

        board.black.d_slot.manual_move("d", 5)

        assert board.black.en_passant_target == ("d", 6)

    def test_pawn_moving_one_square_does_not_set_en_passant_target(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        board.white.e_slot.manual_move("e", 3)

        assert board.white.en_passant_target is None

    def test_pawn_cannot_capture_en_passant_if_target_has_expired(self, default_board):
        default_board.white.d_slot.manual_move("d", 4)
        default_board.black.g_slot.manual_move("g", 6)
        default_board.white.d_slot.manual_move("d", 5)
        default_board.black.e_slot.manual_move("e", 5)

        assert default_board.black.en_passant_target == ("e", 6)

        # Waiting move
        default_board.white.queen.manual_move("d", 2)
        default_board.black.g_slot.manual_move("g", 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white.d_slot.manual_move("e", 6)

    def test_pawn_cannot_capture_en_passant_if_target_did_not_advance_two_squares(
        self, default_board
    ):
        default_board.white.d_slot.manual_move("d", 4)
        default_board.black.g_slot.manual_move("g", 6)
        default_board.white.d_slot.manual_move("d", 5)
        default_board.black.e_slot.manual_move("e", 6)

        # Waiting move
        default_board.white.queen.manual_move("d", 2)
        default_board.black.e_slot.manual_move("e", 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white.d_slot.manual_move("e", 6)

    def test_capturing_en_passant_results_in_expected_state(self, default_board):
        default_board.white.d_slot.manual_move("d", 4)
        default_board.black.g_slot.manual_move("g", 6)
        default_board.white.d_slot.manual_move("d", 5)
        default_board.black.e_slot.manual_move("e", 5)

        # En passant
        default_board.white.d_slot.manual_move("e", 6)

        assert default_board.white.d_slot.position == ("e", 6)
        assert default_board.black.graveyard.e_slot
        assert default_board.black.en_passant_target is None

        halfmove = default_board.game_tree.get_latest_halfmove()
        assert halfmove.change == {
            "WHITE": {
                "d_slot": {
                    "old_position": ("d", 5),
                    "new_position": ("e", 6),
                },
            },
            "BLACK": {
                "en_passant_target": (("e", 6), None),
                "e_slot": {
                    "old_position": ("e", 5),
                    "new_position": None,
                },
            },
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": "",
        }

    def test_rollback_en_passant_results_in_expected_state(self, default_board):
        default_board.white.d_slot.manual_move("d", 4)
        default_board.black.g_slot.manual_move("g", 6)
        default_board.white.d_slot.manual_move("d", 5)
        default_board.black.e_slot.manual_move("e", 5)

        # En passant
        default_board.white.d_slot.manual_move("e", 6)
        default_board.rollback_halfmove()

        assert default_board.white.d_slot.position == ("d", 5)
        assert default_board.black.e_slot.position == ("e", 5)
        assert default_board.black.en_passant_target == ("e", 6)
