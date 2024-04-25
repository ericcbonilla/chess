from main.board import Board
from main.pieces import King, Queen, Rook, WhitePawn


class TestBoard:
    def test_added_pawn_has_correct_name(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="c", y=4),
                King(board=board, team=board.black, x="e", y=5),
                WhitePawn(board=board, team=board.white, x="f", y=2),
            ]
        )

        assert "FP" in board.white

    def test_second_added_queen_has_correct_name(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="c", y=4),
                King(board=board, team=board.black, x="e", y=5),
                Queen(board=board, team=board.white, x="g", y=5),
                Queen(board=board, team=board.black, x="g", y=4),
                Queen(board=board, team=board.white, x="g", y=3),
            ]
        )

        assert "Q2" in board.white
        assert board.white["Q2"].position == ("g", 3)

    # def test_multiple_pawns_on_same_column_have_correct_names(self):
    #     board = Board()
    #     board.add_pieces([
    #         King(board=board, team=board.white, x='c', y=4),
    #         King(board=board, team=board.black, x='e', y=5),
    #         BlackPawn(board=board, team=board.black, x='e', y=7),
    #         BlackPawn(board=board, team=board.black, x='e', y=6),
    #     ])
    #
    #     assert 'EP' in board.black
    #     assert 'FP' in board.black

    def test_when_king_added_on_starting_square_has_moved_false(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=1),
                King(board=board, team=board.black, x="e", y=8),
            ]
        )

        assert not board.white["K"].has_moved
        assert not board.black["K"].has_moved

    def test_when_king_added_not_on_starting_square_has_moved_true(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=2),
                King(board=board, team=board.black, x="e", y=7),
            ]
        )

        assert board.white["K"].has_moved
        assert board.black["K"].has_moved

    def test_when_rook_added_on_starting_square_has_moved_false(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=1),
                King(board=board, team=board.black, x="e", y=8),
                Rook(board=board, team=board.black, x="a", y=8),
                Rook(board=board, team=board.black, x="h", y=8),
            ]
        )

        assert not board.black["R1"].has_moved
        assert not board.black["R2"].has_moved

    def test_when_rook_added_not_on_starting_square_has_moved_true(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=1),
                King(board=board, team=board.black, x="e", y=8),
                Rook(board=board, team=board.black, x="a", y=1),
                Rook(board=board, team=board.black, x="h", y=1),
            ]
        )

        assert board.black["R1"].has_moved
        assert board.black["R2"].has_moved

    def test_apply_three_fullmove_tree_results_in_expected_state(
        self, default_board, three_fullmove_tree
    ):
        default_board.apply_gametree(three_fullmove_tree)

        assert default_board.white["EP"].position == ("e", 4)
        assert default_board.black["EP"].position == ("e", 5)
        assert default_board.white["N2"].position == ("f", 3)
        assert default_board.black["N1"].position == ("c", 6)
        assert default_board.white["B2"].position == ("b", 5)
        assert default_board.black["AP"].position == ("a", 6)

    def test_rollback_first_move_results_in_expected_state(
        self, default_board, half_move_tree
    ):
        default_board.apply_gametree(half_move_tree)

        default_board.rollback_halfmove()

        assert default_board.white["EP"].position == ("e", 2)

    def test_rollback_two_halfmoves_results_in_expected_state(
        self, default_board, three_fullmove_tree, two_fullmove_tree
    ):
        default_board.apply_gametree(three_fullmove_tree)

        default_board.rollback_halfmove()
        default_board.rollback_halfmove()

        assert default_board.game_tree == two_fullmove_tree

        # These pieces should be unchanged
        assert default_board.white["EP"].position == ("e", 4)
        assert default_board.black["EP"].position == ("e", 5)
        assert default_board.white["N2"].position == ("f", 3)
        assert default_board.black["N1"].position == ("c", 6)

        # These should be reverted to their prior positions
        assert default_board.white["B2"].position == ("f", 1)
        assert default_board.black["AP"].position == ("a", 7)

    def test_apply_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)

        assert default_board.white["EP"].position == ("d", 5)
        assert "DP" not in default_board.black
        assert "DP" in default_board.black_graveyard

    def test_rollback_capture_results_in_expected_state(
        self, default_board, one_fullmove_then_capture_tree
    ):
        default_board.apply_gametree(one_fullmove_then_capture_tree)
        default_board.rollback_halfmove()

        assert default_board.white["EP"].position == ("e", 4)
        assert default_board.black["DP"].position == ("d", 5)
        assert "DP" not in default_board.black_graveyard
