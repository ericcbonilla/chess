import pytest

from main.exceptions import InvalidMoveError
from main.pieces import Bishop, King, Knight, Queen, Rook, WhitePawn
from main.x import A, B, C, D, E, F, G, H


class TestCastling:
    def test_king_cant_move_to_its_own_square(self, default_board):
        with pytest.raises(InvalidMoveError):
            default_board.white.move("king", E, 1)

    def test_white_kingside_castle(self, default_board):
        default_board.white.move("g_knight", F, 3)
        default_board.black.move("b_knight", C, 6)
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("b_knight", B, 8)
        default_board.white.move("f_bishop", D, 3)
        default_board.black.move("b_knight", C, 6)
        default_board.white.move("king", G, 1)

        assert default_board.white.king.position == (G, 1)
        assert default_board.white.king.has_moved
        assert default_board.white.h_rook.position == (F, 1)
        assert default_board.white.h_rook.has_moved

    def test_rollback_castle_results_in_expected_state(self, default_board):
        default_board.white.move("g_knight", F, 3)
        default_board.black.move("b_knight", C, 6)
        default_board.white.move("e_pawn", E, 4)
        default_board.black.move("b_knight", B, 8)
        default_board.white.move("f_bishop", D, 3)
        default_board.black.move("b_knight", C, 6)
        default_board.white.move("king", G, 1)

        default_board.rollback_halfmove()

        assert default_board.white.king.position == (E, 1)
        assert not default_board.white.king.has_moved
        assert default_board.white.h_rook.position == (H, 1)
        assert not default_board.white.h_rook.has_moved

    def test_cant_castle_if_king_has_moved(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": H, "y": 1},
                {"piece_type": Rook, "x": A, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
            ],
        )

        board.white.move("king", E, 2)
        board.black.move("king", E, 7)
        board.white.move("king", E, 1)
        board.black.move("king", E, 8)

        with pytest.raises(InvalidMoveError):
            board.white.move("king", G, 1)

    def test_cant_castle_through_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": H, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Queen, "x": F, "y": 6},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", G, 1)  # Can't castle

        board.white.move("a_pawn", A, 4)
        board.black.move("queen", D, 6)
        board.white.move("king", G, 1)  # Now we can castle
        assert board.white.king.position == (G, 1)
        assert board.white.h_rook.position == (F, 1)

    def test_cant_castle_out_of_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 4},
                {"piece_type": Queen, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Rook, "x": B, "y": 8},
                {"piece_type": Rook, "x": H, "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", G, 8)

    def test_cant_castle_into_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": B, "y": 1},
                {"piece_type": Bishop, "x": B, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Rook, "x": A, "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", C, 8)

    def test_cant_castle_into_check_from_king(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": B, "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Rook, "x": A, "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", C, 8)

    def test_cant_castle_if_skewered(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 4},
                {"piece_type": Queen, "x": A, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Rook, "x": B, "y": 1},
                {"piece_type": Rook, "x": H, "y": 8},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", G, 8)

    def test_doesnt_castle_when_king_is_not_moving_from_starting_square(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": F, "y": 2},
                {"piece_type": Rook, "x": H, "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Rook, "x": G, "y": 2},
            ],
        )

        board.white.move("king", G, 2)
        assert board.white.h_rook.position == (H, 5)

    def test_king_cant_castle_through_closed_path(self, default_board):
        with pytest.raises(InvalidMoveError):
            default_board.white.move("king", G, 1)


class TestKingScenarios:
    def test_king_cannot_move_multiple_squares_if_not_castling(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", E, 3)

    def test_when_king_added_on_starting_square_has_moved_false(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
            ],
        )

        assert not board.white.king.has_moved
        assert not board.black.king.has_moved

    def test_when_king_added_not_on_starting_square_has_moved_true(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 7},
            ],
        )

        assert board.white.king.has_moved
        assert board.black.king.has_moved

    def test_white_king_put_in_check(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("e_pawn", E, 6)
        default_board.white.move("g_knight", F, 3)
        default_board.black.move("f_bishop", B, 4)

        assert default_board.white.king.is_in_check()

    def test_cant_move_into_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 1},
                {"piece_type": Rook, "x": H, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 8},
                {"piece_type": Queen, "x": F, "y": 6},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", F, 2)  # Can't move
        board.white.move("a_pawn", A, 4)

        board.black.move("queen", G, 7)
        board.white.move("king", F, 2)  # Now we can move
        assert board.white.king.position == (F, 2)

    def test_king_cant_move_next_to_king(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": C, "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
            ],
            active_color="b",
        )

        with pytest.raises(InvalidMoveError):
            board.black.move("king", D, 4)

    def test_cant_leave_king_in_check(self, default_board):
        default_board.white.move("d_pawn", D, 4)
        default_board.black.move("c_pawn", C, 6)
        default_board.white.move("h_pawn", H, 3)
        default_board.black.move("queen", A, 5)  # Check!

        with pytest.raises(InvalidMoveError):
            default_board.white.move("b_knight", A, 3)  # Won't work

        default_board.white.move("b_knight", C, 3)  # Works
        assert default_board.white.b_knight.position == (C, 3)

    def test_discovered_check(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": D, "y": 4},
                {"piece_type": Rook, "x": D, "y": 8},
            ],
            black_data=[
                {"piece_type": King, "x": D, "y": 1},
            ],
        )
        halfmove = board.white.move("king", C, 3)

        assert halfmove.change["check"]
        assert board.white.a_rook.position == (D, 8)
        assert board.black.king.is_in_check()

    def test_cant_leave_king_in_check_from_pawn(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 5},
                {"piece_type": WhitePawn, "x": F, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Queen, "x": H, "y": 5},
            ],
        )

        board.white.move("f_pawn", F, 4)

        with pytest.raises(InvalidMoveError):
            board.black.move("queen", H, 4)

    def test_king_cant_move_into_check_from_pawn_even_if_discovered_check(
        self, builder
    ):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 5},
                {"piece_type": WhitePawn, "x": F, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": E, "y": 5},
                {"piece_type": Queen, "x": H, "y": 5},
            ],
            active_color="b",
        )

        # Would be discovered check if not for the pawn
        with pytest.raises(InvalidMoveError):
            board.black.move("king", E, 4)

    def test_cant_leave_king_in_check_from_knight(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 3},
                {"piece_type": WhitePawn, "x": B, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
                {"piece_type": Knight, "x": F, "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("b_pawn", B, 4)

    def test_cant_move_into_check_from_knight(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
                {"piece_type": Knight, "x": F, "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", E, 3)

    def test_cant_move_backwards_if_skewered(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": E, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
                {"piece_type": Bishop, "x": G, "y": 5},
            ],
        )

        with pytest.raises(InvalidMoveError):
            board.white.move("king", D, 2)

    def test_cant_move_toward_attacker_when_cornered_on_diagonal(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
                {"piece_type": Rook, "x": B, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": H, "y": 8},
                {"piece_type": Bishop, "x": H, "y": 6},
            ],
            active_color="b",
        )

        board.black.move("c_bishop", G, 7)

        with pytest.raises(InvalidMoveError):
            board.white.move("king", B, 2)
