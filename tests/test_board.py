from main.agents import ManualAgent
from main.builders import BoardBuilder
from main.pieces import King, Queen, Rook, WhitePawn


class TestBoardBuilder:
    def test_added_pawn_has_correct_name(self):
        builder = BoardBuilder()
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

        assert board.white.f_pawn

    def test_second_added_queen_has_correct_name(self):
        builder = BoardBuilder()
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
        assert board.white.g_prom.position == ("g", 4)
        assert board.white.h_prom.position == ("g", 3)

    # TODO
    # def test_multiple_pawns_on_same_column_have_correct_names(self):
    #     board = Board()
    #     board.add_pieces([
    #         King(board=board, agent=board.white, x='c', y=4),
    #         King(board=board, agent=board.black, x='e', y=5),
    #         BlackPawn(board=board, agent=board.black, x='e', y=7),
    #         BlackPawn(board=board, agent=board.black, x='e', y=6),
    #     ])
    #
    #     assert 'EP' in board.black
    #     assert 'FP' in board.black

    def test_when_king_added_on_starting_square_has_moved_false(self):
        builder = BoardBuilder()
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        assert not board.white.king.has_moved
        assert not board.black.king.has_moved

    def test_when_king_added_not_on_starting_square_has_moved_true(self):
        builder = BoardBuilder()
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "e", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 7},
            ],
        )

        assert board.white.king.has_moved
        assert board.black.king.has_moved

    def test_when_rook_added_on_starting_square_has_moved_false(self):
        builder = BoardBuilder()
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

    def test_when_rook_added_not_on_starting_square_has_moved_true(self):
        builder = BoardBuilder()
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
