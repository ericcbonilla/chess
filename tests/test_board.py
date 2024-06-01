from main.agents import ManualAgent
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook


class TestBoard:
    def test_apply_three_fullmove_tree_results_in_expected_state(
        self, default_board, three_fullmove_tree
    ):
        default_board.apply_gametree(three_fullmove_tree)

        assert default_board.white.e_pawn.position == ("e", 4)
        assert default_board.black.e_pawn.position == ("e", 5)
        assert default_board.white.g_knight.position == ("f", 3)
        assert default_board.black.b_knight.position == ("c", 6)
        assert default_board.white.f_bishop.position == ("b", 5)
        assert default_board.black.a_pawn.position == ("a", 6)

    def test_rollback_first_move_results_in_expected_state(
        self, default_board, half_move_tree
    ):
        default_board.apply_gametree(half_move_tree)

        default_board.rollback_halfmove()

        assert default_board.white.e_pawn.position == ("e", 2)

    def test_rollback_two_halfmoves_results_in_expected_state(
        self, default_board, three_fullmove_tree, two_fullmove_tree
    ):
        default_board.apply_gametree(three_fullmove_tree)

        default_board.rollback_halfmove()
        default_board.rollback_halfmove()

        assert default_board.game_tree == two_fullmove_tree

        # These pieces should be unchanged
        assert default_board.white.e_pawn.position == ("e", 4)
        assert default_board.black.e_pawn.position == ("e", 5)
        assert default_board.white.g_knight.position == ("f", 3)
        assert default_board.black.b_knight.position == ("c", 6)

        # These should be reverted to their prior positions
        assert default_board.white.f_bishop.position == ("f", 1)
        assert default_board.black.a_pawn.position == ("a", 7)

    def test_apply_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)

        assert default_board.white.e_pawn.position == ("d", 5)
        assert default_board.black.d_pawn is None
        assert default_board.black.graveyard.d_pawn

    def test_rollback_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)
        default_board.rollback_halfmove()

        assert default_board.white.e_pawn.position == ("e", 4)
        assert default_board.black.d_pawn.position == ("d", 5)
        assert default_board.black.graveyard.d_pawn is None

    def test_with_single_move_get_fen_returns_expected(self, default_board):
        default_board.white.e_pawn.manual_move("e", 4)

        assert default_board.get_fen() == (
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        )

    def test_get_fen_for_specific_move_returns_expected(self, default_board):
        default_board.white.d_pawn.manual_move("d", 4)
        default_board.black.e_pawn.manual_move("e", 6)
        default_board.white.g_knight.manual_move("f", 3)
        default_board.black.f_bishop.manual_move("a", 3)
        default_board.white.g_pawn.manual_move("g", 3)

        assert default_board.get_fen(2.5) == (
            "rnbqk1nr/pppp1ppp/4p3/8/3P4/b4N2/PPP1PPPP/RNBQKB1R w KQkq - 2 3"
        )

    def test_get_fen_for_last_move_returns_expected(self, default_board):
        default_board.white.d_pawn.manual_move("d", 4)
        default_board.black.e_pawn.manual_move("e", 6)

        assert default_board.get_fen(1.5) == (
            "rnbqkbnr/pppp1ppp/4p3/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d3 0 2"
        )


class TestHasInsufficientMaterial:
    def test_kkp_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": BlackPawn, "x": "a", "y": 3},
                {"piece_type": Rook, "x": "d", "y": 2},
            ],
        )
        halfmove = board.white.king.manual_move("d", 2)

        assert halfmove.change["game_result"] is None

    def test_kkppp_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": BlackPawn, "x": "a", "y": 3},
                {"piece_type": BlackPawn, "x": "g", "y": 3},
                {"piece_type": BlackPawn, "x": "h", "y": 3},
                {"piece_type": Rook, "x": "d", "y": 2},
            ],
        )
        halfmove = board.white.king.manual_move("d", 2)

        assert halfmove.change["game_result"] is None

    def test_kk_yields_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
            ],
            active_color="b",
        )
        halfmove = board.black.king.manual_move("d", 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kbk_yields_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "h", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
            ],
            active_color="b",
        )
        halfmove = board.black.king.manual_move("d", 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kkn_yields_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Rook, "x": "d", "y": 2},
                {"piece_type": Knight, "x": "b", "y": 6},
            ],
        )
        halfmove = board.white.king.manual_move("d", 2)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kbkn_yields_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "a", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Knight, "x": "b", "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.king.manual_move("d", 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"


class TestHalfmoveClock:
    def test_when_pawn_moves_halfmove_clock_is_reset(
        self, default_board, two_fullmove_tree
    ):
        default_board.apply_gametree(two_fullmove_tree)
        assert default_board.halfmove_clock == 2

        default_board.white.h_pawn.manual_move("h", 4)

        assert default_board.halfmove_clock == 0

    def test_when_piece_is_captured_halfmove_clock_is_reset(self, default_board):
        default_board.white.b_knight.manual_move("c", 3)
        default_board.black.g_knight.manual_move("f", 6)
        default_board.white.b_knight.manual_move("e", 4)
        assert default_board.halfmove_clock == 3

        default_board.black.g_knight.manual_move("e", 4)

        assert default_board.halfmove_clock == 0

    def test_when_other_piece_is_moved_halfmove_clock_increments(self, default_board):
        default_board.white.b_knight.manual_move("c", 3)
        default_board.black.g_knight.manual_move("f", 6)
        default_board.white.b_knight.manual_move("e", 4)
        assert default_board.halfmove_clock == 3

        default_board.black.g_knight.manual_move("d", 5)

        assert default_board.halfmove_clock == 4

    def test_when_75th_move_is_pawn_move_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "a", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": BlackPawn, "x": "a", "y": 6},
                {"piece_type": Knight, "x": "b", "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.a_pawn.manual_move("a", 5)

        assert board.halfmove_clock == 0
        assert halfmove.change["game_result"] is None

    def test_when_75th_move_is_capture_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "a", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": BlackPawn, "x": "a", "y": 6},
                {"piece_type": Knight, "x": "b", "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.king.manual_move("d", 3)

        assert board.halfmove_clock == 0
        assert halfmove.change["game_result"] is None

    def test_when_75th_move_is_regular_move_yields_draw(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "a", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": BlackPawn, "x": "a", "y": 6},
                {"piece_type": Knight, "x": "b", "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.king.manual_move("b", 4)

        assert board.halfmove_clock == 125
        assert halfmove.change["game_result"] == "½-½ Seventy-five-move rule"

    def test_when_75th_move_is_checkmate_yields_checkmate(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 3},
                {"piece_type": Queen, "x": "a", "y": 2},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.queen.manual_move("e", 2)

        assert board.halfmove_clock == 125
        assert halfmove.change["game_result"] == "0-1"
