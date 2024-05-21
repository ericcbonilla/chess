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
