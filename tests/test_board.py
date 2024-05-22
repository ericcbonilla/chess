from main.agents import ManualAgent
from main.pieces import Bishop, BlackPawn, King, Knight, Rook


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

        board.white.king.manual_move("d", 2)

        halfmove = board.game_tree.get_latest_halfmove()
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

        board.white.king.manual_move("d", 2)

        halfmove = board.game_tree.get_latest_halfmove()
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
        )

        board.black.king.manual_move("d", 3)

        halfmove = board.game_tree.get_latest_halfmove()
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
        )

        board.black.king.manual_move("d", 3)

        halfmove = board.game_tree.get_latest_halfmove()
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

        board.white.king.manual_move("d", 2)

        halfmove = board.game_tree.get_latest_halfmove()
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
        )

        board.black.king.manual_move("d", 3)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change["game_result"] == "½-½ Insufficient material"
