from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook
from main.x import A, B, C, D, E, F, G, H


class TestBoard:
    def test_apply_three_fullmove_tree_results_in_expected_state(
        self, default_board, three_fullmove_tree
    ):
        default_board.apply_gametree(three_fullmove_tree)

        assert default_board.white.e_pawn.position == (E, 4)
        assert default_board.black.e_pawn.position == (E, 5)
        assert default_board.white.g_knight.position == (F, 3)
        assert default_board.black.b_knight.position == (C, 6)
        assert default_board.white.f_bishop.position == (B, 5)
        assert default_board.black.a_pawn.position == (A, 6)

    def test_rollback_first_move_results_in_expected_state(
        self, default_board, half_move_root
    ):
        default_board.apply_gametree(half_move_root)

        default_board.rollback_halfmove()

        assert default_board.white.e_pawn.position == (E, 2)

    def test_rollback_two_halfmoves_results_in_expected_state(
        self, default_board, three_fullmove_tree, two_fullmove_root
    ):
        default_board.apply_gametree(three_fullmove_tree)

        default_board.rollback_halfmove()
        default_board.rollback_halfmove()

        assert default_board.game_tree.root == two_fullmove_root

        # These pieces should be unchanged
        assert default_board.white.e_pawn.position == (E, 4)
        assert default_board.black.e_pawn.position == (E, 5)
        assert default_board.white.g_knight.position == (F, 3)
        assert default_board.black.b_knight.position == (C, 6)

        # These should be reverted to their prior positions
        assert default_board.white.f_bishop.position == (F, 1)
        assert default_board.black.a_pawn.position == (A, 7)

    def test_apply_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)

        assert default_board.white.e_pawn.position == (D, 5)
        assert default_board.black.d_pawn is None
        assert default_board.black.graveyard.d_pawn

    def test_rollback_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)
        default_board.rollback_halfmove()

        assert default_board.white.e_pawn.position == (E, 4)
        assert default_board.black.d_pawn.position == (D, 5)
        assert default_board.black.graveyard.d_pawn is None

    def test_with_single_move_get_fen_returns_expected(self, default_board):
        default_board.white.move("e_pawn", E, 4)

        assert default_board.get_fen(internal=True) == (
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        )

    def test_get_fen_for_specific_move_returns_expected(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("e_pawn", E, 6)
        default_board.white.move("g_knight", F, 3)
        default_board.black.move("f_bishop", A, 3)
        default_board.white.move("g_pawn", G, 3)

        assert default_board.get_fen(2.5, internal=True) == (
            "rnbqk1nr/pppp1ppp/4p3/8/3P4/b4N2/PPP1PPPP/RNBQKB1R w KQkq - 2 3"
        )

    def test_get_fen_for_last_move_returns_expected(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("e_pawn", E, 6)

        assert default_board.get_fen(1.5, internal=True) == (
            "rnbqkbnr/pppp1ppp/4p3/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2"
        )


class TestHasInsufficientMaterial:
    def test_kkp_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": BlackPawn, "x": A, "y": 3},
                {"piece_type": Rook, "x": D, "y": 2},
            ],
        )
        board.fullmove_number = 20
        halfmove = board.white.move("king", D, 2)

        assert halfmove.change["game_result"] is None

    def test_kkppp_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": BlackPawn, "x": A, "y": 3},
                {"piece_type": BlackPawn, "x": G, "y": 3},
                {"piece_type": BlackPawn, "x": H, "y": 3},
                {"piece_type": Rook, "x": D, "y": 2},
            ],
        )
        board.fullmove_number = 20
        halfmove = board.white.move("king", D, 2)

        assert halfmove.change["game_result"] is None

    def test_kk_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
            ],
            active_color="b",
        )
        board.fullmove_number = 20
        halfmove = board.black.move("king", D, 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kbk_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": H, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
            ],
            active_color="b",
        )
        board.fullmove_number = 20
        halfmove = board.black.move("king", D, 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kkn_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": Rook, "x": D, "y": 2},
                {"piece_type": Knight, "x": B, "y": 6},
            ],
        )
        board.fullmove_number = 20
        halfmove = board.white.move("king", D, 2)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"

    def test_kbkn_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": Knight, "x": B, "y": 6},
            ],
            active_color="b",
        )
        board.fullmove_number = 20
        halfmove = board.black.move("king", D, 3)

        assert halfmove.change["game_result"] is None

    def test_kbkb_same_color_bishops_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": Bishop, "x": B, "y": 5},
            ],
            active_color="b",
        )
        board.fullmove_number = 20
        halfmove = board.black.move("king", D, 3)

        assert halfmove.change["game_result"] == "½-½ Insufficient material"


class TestHalfmoveClock:
    def test_when_pawn_moves_halfmove_clock_is_reset(
        self, default_board, two_fullmove_root
    ):
        default_board.apply_gametree(two_fullmove_root)
        assert default_board.halfmove_clock == 2

        default_board.white.move("h_pawn", H, 4)

        assert default_board.halfmove_clock == 0

    def test_when_piece_is_captured_halfmove_clock_is_reset(self, default_board):
        default_board.white.move("b_knight", C, 3)
        default_board.black.move("g_knight", F, 6)
        default_board.white.move("b_knight", E, 4)
        assert default_board.halfmove_clock == 3

        default_board.black.move("g_knight", E, 4)

        assert default_board.halfmove_clock == 0

    def test_when_other_piece_is_moved_halfmove_clock_increments(self, default_board):
        default_board.white.move("b_knight", C, 3)
        default_board.black.move("g_knight", F, 6)
        default_board.white.move("b_knight", E, 4)
        assert default_board.halfmove_clock == 3

        default_board.black.move("g_knight", D, 5)

        assert default_board.halfmove_clock == 4

    def test_when_75th_move_is_pawn_move_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": BlackPawn, "x": A, "y": 6},
                {"piece_type": Knight, "x": B, "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.move("a_pawn", A, 5)

        assert board.halfmove_clock == 0
        assert halfmove.change["game_result"] is None

    def test_when_75th_move_is_capture_does_not_yield_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": BlackPawn, "x": A, "y": 6},
                {"piece_type": Knight, "x": B, "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.move("king", D, 3)

        assert board.halfmove_clock == 0
        assert halfmove.change["game_result"] is None

    def test_when_75th_move_is_regular_move_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
                {"piece_type": Bishop, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 4},
                {"piece_type": BlackPawn, "x": A, "y": 6},
                {"piece_type": Knight, "x": B, "y": 6},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.move("king", B, 4)

        assert board.halfmove_clock == 125
        assert halfmove.change["game_result"] == "½-½ Seventy-five-move rule"

    def test_when_75th_move_is_checkmate_yields_checkmate(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 3},
                {"piece_type": Queen, "x": A, "y": 2},
            ],
            active_color="b",
        )
        board.halfmove_clock = 124
        halfmove = board.black.move("queen", E, 2)

        assert board.halfmove_clock == 125
        assert halfmove.change["game_result"] == "0-1"


class TestDrawByRepetition:
    def test_when_starting_position_occurs_three_times_yields_draw(self, default_board):
        # First "repetition" includes the starting position
        default_board.white.move("b_knight", C, 3)
        default_board.black.move("b_knight", C, 6)

        # Two
        default_board.white.move("b_knight", B, 1)
        default_board.black.move("b_knight", B, 8)
        default_board.white.move("b_knight", C, 3)
        halfmove = default_board.black.move("b_knight", C, 6)

        assert halfmove.change["game_result"] is None

        # Three
        default_board.white.move("b_knight", B, 1)
        halfmove = default_board.black.move("b_knight", B, 8)

        assert halfmove.change["game_result"] == "½-½ Repetition"

    def test_when_midgame_position_occurs_three_times_yields_draw(self, builder):
        board = builder.from_fen(
            "r1bq1rk1/ppppnppp/2n5/1B2p3/1b2P3/2N2P2/PPPPN1PP/R1BQ1RK1 b - - 8 6"
        )

        board.black.move("f_bishop", A, 5)
        board.white.move("c_bishop", A, 4)

        # Two
        board.black.move("f_bishop", B, 4)
        board.white.move("c_bishop", B, 5)
        board.black.move("f_bishop", A, 5)
        halfmove = board.white.move("c_bishop", A, 4)

        assert halfmove.change["game_result"] is None

        # Three
        board.black.move("f_bishop", B, 4)
        halfmove = board.white.move("c_bishop", B, 5)

        assert halfmove.change["game_result"] == "½-½ Repetition"

    def test_when_endgame_position_occurs_three_times_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": D, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": C, "y": 5},
            ],
            active_color="w",
        )

        board.white.move("a_rook", C, 3)
        board.black.move("king", D, 5)

        # Two
        board.white.move("a_rook", D, 3)
        board.black.move("king", C, 5)
        board.white.move("a_rook", C, 3)
        halfmove = board.black.move("king", D, 5)

        assert halfmove.change["game_result"] is None

        # Three
        board.white.move("a_rook", D, 3)
        halfmove = board.black.move("king", C, 5)

        assert halfmove.change["game_result"] == "½-½ Repetition"

    def test_when_nonsuccessive_position_occurs_three_times_yields_draw(self, builder):
        board = builder.from_fen(
            "r1bq1rk1/ppppnppp/2n5/1B2p3/1b2P3/2N2P2/PPPPN1PP/R1BQ1RK1 b - - 8 6"
        )

        board.black.move("f_bishop", A, 5)
        board.white.move("c_bishop", C, 4)

        # Additional moves
        board.black.move("h_rook", E, 8)
        board.white.move("h_rook", E, 1)
        board.black.move("h_rook", F, 8)
        board.white.move("h_rook", F, 1)

        # Two
        board.black.move("f_bishop", B, 4)
        board.white.move("c_bishop", B, 5)
        board.black.move("f_bishop", A, 5)
        halfmove = board.white.move("c_bishop", A, 4)

        assert halfmove.change["game_result"] is None

        # Three
        board.black.move("f_bishop", B, 4)
        halfmove = board.white.move("c_bishop", B, 5)

        assert halfmove.change["game_result"] == "½-½ Repetition"
