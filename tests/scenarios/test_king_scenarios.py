import pytest

from main.exceptions import InvalidMoveError
from main.pieces import Bishop, King, Knight, Queen, Rook, WhitePawn


class TestCastling:
    def test_white_kingside_castle(self, default_board):
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("b_knight", "c", 6)
        default_board.white.move("e_pawn", "e", 4)
        default_board.black.move("b_knight", "b", 8)
        default_board.white.move("f_bishop", "d", 3)
        default_board.black.move("b_knight", "c", 6)
        default_board.white.move("king", "g", 1)

        assert default_board.white.king.position == ("g", 1)
        assert default_board.white.king.has_moved
        assert default_board.white.h_rook.position == ("f", 1)
        assert default_board.white.h_rook.has_moved

    def test_rollback_castle_results_in_expected_state(self, default_board):
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("b_knight", "c", 6)
        default_board.white.move("e_pawn", "e", 4)
        default_board.black.move("b_knight", "b", 8)
        default_board.white.move("f_bishop", "d", 3)
        default_board.black.move("b_knight", "c", 6)
        default_board.white.move("king", "g", 1)

        default_board.rollback_halfmove()

        assert default_board.white.king.position == ("e", 1)
        assert not default_board.white.king.has_moved
        assert default_board.white.h_rook.position == ("h", 1)
        assert not default_board.white.h_rook.has_moved

    def test_cant_castle_if_king_has_moved(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 1},
                {"piece_type": Rook, "x": "a", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        board.white.move("king", "e", 2)
        board.black.move("king", "e", 7)
        board.white.move("king", "e", 1)
        board.black.move("king", "e", 8)

        with pytest.raises(InvalidMoveError):
            board.white.move("king", "g", 1)

    def test_cant_castle_through_check(self, default_board):
        # TODO rewrite these verbose tests
        default_board.white.move("f_pawn", "f", 4)
        default_board.black.move("g_pawn", "g", 5)
        default_board.white.move("g_pawn", "g", 3)
        default_board.black.move("e_pawn", "e", 6)
        default_board.white.move("f_pawn", "g", 5)
        default_board.black.move("queen", "f", 6)
        default_board.white.move("g_knight", "h", 3)
        default_board.black.move("a_pawn", "a", 6)
        default_board.white.move("f_bishop", "g", 2)
        default_board.black.move("b_pawn", "b", 6)

        with pytest.raises(InvalidMoveError):
            default_board.white.move("king", "g", 1)  # Can't castle
        assert default_board.black.queen.position == ("f", 6)

        default_board.white.move("a_pawn", "a", 3)
        default_board.black.move("queen", "g", 7)
        default_board.white.move("king", "g", 1)  # Now we can castle
        assert default_board.white.king.position == ("g", 1)
        assert default_board.white.h_rook.position == ("f", 1)

    def test_cant_castle_out_of_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 4},
                {"piece_type": Queen, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "b", "y": 8},
                {"piece_type": Rook, "x": "h", "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", "g", 8)

    def test_cant_castle_if_skewered(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 4},
                {"piece_type": Queen, "x": "a", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "b", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", "g", 8)

    def test_doesnt_castle_when_king_is_not_moving_from_starting_square(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "f", "y": 2},
                {"piece_type": Rook, "x": "h", "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Rook, "x": "g", "y": 2},
            ],
        )

        board.white.move("king", "g", 2)
        assert board.white.h_rook.position == ("h", 5)


class TestKingScenarios:
    def test_when_king_added_on_starting_square_has_moved_false(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        assert not board.white.king.has_moved
        assert not board.black.king.has_moved

    def test_when_king_added_not_on_starting_square_has_moved_true(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 7},
            ],
        )

        assert board.white.king.has_moved
        assert board.black.king.has_moved

    def test_white_king_put_in_check(self, default_board):
        default_board.white.move("d_pawn", "d", 4)
        default_board.black.move("e_pawn", "e", 6)
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("f_bishop", "b", 4)

        assert default_board.white.king.is_in_check()

    def test_cant_move_into_check(self, default_board):
        default_board.white.move("f_pawn", "f", 4)
        default_board.black.move("g_pawn", "g", 5)
        default_board.white.move("g_pawn", "g", 3)
        default_board.black.move("e_pawn", "e", 6)
        default_board.white.move("f_pawn", "g", 5)
        default_board.black.move("queen", "f", 6)
        default_board.white.move("g_knight", "h", 3)
        default_board.black.move("a_pawn", "a", 6)
        default_board.white.move("f_bishop", "g", 2)
        default_board.black.move("b_pawn", "b", 6)

        with pytest.raises(InvalidMoveError):
            default_board.white.move("king", "f", 2)  # Can't move

        default_board.white.move("c_pawn", "c", 3)
        default_board.black.move("queen", "g", 7)
        default_board.white.move("king", "f", 2)
        assert default_board.white.king.position == ("f", 2)

    def test_king_cant_move_next_to_king(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", "d", 4)

    def test_cant_leave_king_in_check(self, default_board):
        default_board.white.move("d_pawn", "d", 4)
        default_board.black.move("c_pawn", "c", 6)
        default_board.white.move("h_pawn", "h", 3)
        default_board.black.move("queen", "a", 5)  # Check!

        with pytest.raises(InvalidMoveError):
            default_board.white.move("b_knight", "a", 3)  # Won't work

        default_board.white.move("b_knight", "c", 3)  # Works
        assert default_board.white.b_knight.position == ("c", 3)

    def test_discovered_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "d", "y": 4},
                {"piece_type": Rook, "x": "d", "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": "d", "y": 1},
            ],
        )
        halfmove = board.white.move("king", "c", 3)

        assert halfmove.change["check"]
        assert board.white.a_rook.position == ("d", 8)
        assert board.black.king.is_in_check()

    def test_cant_leave_king_in_check_from_pawn(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 5},
                {"piece_type": WhitePawn, "x": "f", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Queen, "x": "h", "y": 5},
            ],
        )

        board.white.move("f_pawn", "f", 4)

        with pytest.raises(InvalidMoveError):
            board.black.move("queen", "h", 4)

    def test_king_cant_move_into_check_from_pawn_even_if_discovered_check(
        self, builder
    ):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 5},
                {"piece_type": WhitePawn, "x": "f", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Queen, "x": "h", "y": 5},
            ],
            active_color="b",
        )

        # Would be discovered check if not for the pawn
        with pytest.raises(InvalidMoveError):
            board.black.move("king", "e", 4)

    def test_cant_leave_king_in_check_from_knight(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 3},
                {"piece_type": WhitePawn, "x": "b", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
                {"piece_type": Knight, "x": "f", "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("b_pawn", "b", 4)

    def test_cant_move_into_check_from_knight(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
                {"piece_type": Knight, "x": "f", "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", "e", 3)

    def test_cant_move_backwards_if_skewered(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
                {"piece_type": Bishop, "x": "g", "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", "d", 2)

    def test_cant_move_toward_attacker_when_cornered_on_diagonal(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": WhitePawn, "x": "a", "y": 2},
                {"piece_type": Bishop, "x": "b", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Bishop, "x": "h", "y": 6},
            ],
            active_color="b",
        )

        board.black.move("c_bishop", "g", 7)

        with pytest.raises(InvalidMoveError):
            board.white.move("king", "b", 2)
