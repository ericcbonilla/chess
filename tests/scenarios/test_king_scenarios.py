import pytest

from main.board import Board
from main.exceptions import InvalidMoveError
from main.pieces import Bishop, King, Knight, Queen, Rook, WhitePawn


class TestCastling:
    def test_white_kingside_castle(self, default_board):
        default_board.white["N2"].random_move()
        default_board.white["EP"].random_move()
        default_board.white["B2"].random_move()
        default_board.white["K"].manual_move("g", 1)

        assert default_board.white["K"].position == ("g", 1)
        assert default_board.white["K"].has_moved
        assert default_board.white["R2"].position == ("f", 1)
        assert default_board.white["R2"].has_moved

    def test_rollback_castle_results_in_expected_state(self, default_board):
        default_board.white["N2"].random_move()
        default_board.white["EP"].random_move()
        default_board.white["B2"].random_move()
        default_board.white["K"].manual_move("g", 1)

        default_board.rollback_halfmove()

        assert default_board.white["K"].position == ("e", 1)
        assert not default_board.white["K"].has_moved
        assert default_board.white["R2"].position == ("h", 1)
        assert not default_board.white["R2"].has_moved

    def test_cant_castle_if_king_has_moved(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.black, x="e", y=8),
                King(board=board, team=board.white, x="e", y=1),
                Rook(board=board, team=board.white, x="h", y=1),
                Rook(board=board, team=board.white, x="a", y=1),
            ]
        )

        board.white["K"].manual_move("e", 2)
        board.white["K"].manual_move("e", 1)

        with pytest.raises(InvalidMoveError):
            board.white["K"].manual_move("g", 1)

    def test_cant_castle_through_check(self, default_board):
        default_board.white["FP"].manual_move("f", 4)
        default_board.black["GP"].manual_move("g", 5)
        default_board.white["GP"].manual_move("g", 3)
        default_board.black["EP"].manual_move("e", 6)
        default_board.white["FP"].manual_move("g", 5)
        default_board.black["Q1"].manual_move("f", 6)
        default_board.white["N2"].manual_move("h", 3)
        default_board.black["AP"].manual_move("a", 6)
        default_board.white["B2"].manual_move("g", 2)
        default_board.black["BP"].manual_move("b", 6)

        with pytest.raises(InvalidMoveError):
            default_board.white["K"].manual_move("g", 1)  # Can't castle
        assert default_board.black["Q1"].position == ("f", 6)

        default_board.black["Q1"].manual_move("g", 7)
        default_board.white["K"].manual_move("g", 1)  # Now we can castle
        assert default_board.white["K"].position == ("g", 1)
        assert default_board.white["R2"].position == ("f", 1)

    def test_cant_castle_out_of_check(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="a", y=4),
                Queen(board=board, team=board.white, x="e", y=1),
                King(board=board, team=board.black, x="e", y=8),
                Rook(board=board, team=board.black, x="b", y=8),
                Rook(board=board, team=board.black, x="h", y=8),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.black["K"].manual_move("g", 8)

    def test_cant_castle_if_skewered(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="a", y=4),
                Queen(board=board, team=board.white, x="a", y=8),
                King(board=board, team=board.black, x="e", y=8),
                Rook(board=board, team=board.black, x="b", y=1),
                Rook(board=board, team=board.black, x="h", y=8),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.black["K"].manual_move("g", 8)

    def test_doesnt_castle_when_king_is_not_moving_from_starting_square(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="f", y=2),
                Rook(board=board, team=board.white, x="h", y=5),
                King(board=board, team=board.black, x="e", y=8),
                Rook(board=board, team=board.black, x="g", y=2),
            ]
        )

        board.white["K"].manual_move("g", 2)
        assert board.white["R1"].position == ("h", 5)


class TestKingScenarios:
    def test_white_king_put_in_check(self, default_board):
        default_board.white["DP"].random_move()
        default_board.black["EP"].random_move()
        default_board.white["N2"].random_move()
        default_board.black["B2"].manual_move("b", 4)

        assert default_board.white["K"].is_in_check()

    def test_cant_move_into_check(self, default_board):
        default_board.white["FP"].manual_move("f", 4)
        default_board.black["GP"].manual_move("g", 5)
        default_board.white["GP"].manual_move("g", 3)
        default_board.black["EP"].manual_move("e", 6)
        default_board.white["FP"].manual_move("g", 5)
        default_board.black["Q1"].manual_move("f", 6)
        default_board.white["N2"].manual_move("h", 3)
        default_board.black["AP"].manual_move("a", 6)
        default_board.white["B2"].manual_move("g", 2)
        default_board.black["BP"].manual_move("b", 6)

        with pytest.raises(InvalidMoveError):
            default_board.white["K"].manual_move("f", 2)  # Can't move

        default_board.black["Q1"].manual_move("g", 7)
        default_board.white["K"].manual_move("f", 2)
        assert default_board.white["K"].position == ("f", 2)

    def test_king_cant_move_next_to_king(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="c", y=4),
                King(board=board, team=board.black, x="e", y=5),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.black["K"].manual_move("d", 4)

    def test_cant_leave_king_in_check(self, default_board):
        default_board.white["DP"].manual_move("d", 4)
        default_board.black["CP"].manual_move("c", 6)
        default_board.white["HP"].manual_move("h", 3)
        default_board.black["Q1"].manual_move("a", 5)  # Check!

        with pytest.raises(InvalidMoveError):
            default_board.white["N1"].manual_move("a", 3)  # Won't work

        default_board.white["N1"].manual_move("c", 3)  # Works
        assert default_board.white["N1"].position == ("c", 3)

    def test_discovered_check(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.black, x="d", y=1),
                King(board=board, team=board.white, x="d", y=4),
                Rook(board=board, team=board.white, x="d", y=8),
            ]
        )

        board.white["K"].manual_move("c", 3)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change["check"]
        assert board.white["R1"].position == ("d", 8)
        assert board.black["K"].is_in_check()

    def test_cant_leave_king_in_check_from_pawn(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="a", y=5),
                WhitePawn(board=board, team=board.white, x="f", y=3),
                King(board=board, team=board.black, x="e", y=5),
                Queen(board=board, team=board.black, x="h", y=5),
            ]
        )

        board.white["FP"].manual_move("f", 4)

        with pytest.raises(InvalidMoveError):
            board.black["Q1"].manual_move("h", 4)

    def test_king_cant_move_into_check_from_pawn_even_if_discovered_check(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="a", y=5),
                WhitePawn(board=board, team=board.white, x="f", y=3),
                King(board=board, team=board.black, x="e", y=5),
                Queen(board=board, team=board.black, x="h", y=5),
            ]
        )

        # Would be discovered check if not for the pawn
        with pytest.raises(InvalidMoveError):
            board.black["K"].manual_move("e", 4)

    def test_cant_leave_king_in_check_from_knight(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=3),
                WhitePawn(board=board, team=board.white, x="b", y=3),
                King(board=board, team=board.black, x="a", y=8),
                Knight(board=board, team=board.black, x="f", y=5),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.white["BP"].manual_move("b", 4)

    def test_cant_move_into_check_from_knight(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=4),
                King(board=board, team=board.black, x="a", y=8),
                Knight(board=board, team=board.black, x="f", y=5),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.white["K"].manual_move("e", 3)

    def test_cant_move_backwards_if_skewered(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="e", y=3),
                King(board=board, team=board.black, x="a", y=8),
                Bishop(board=board, team=board.black, x="g", y=5),
            ]
        )

        with pytest.raises(InvalidMoveError):
            board.white["K"].manual_move("d", 2)

    def test_cant_move_toward_attacker_when_cornered_on_diagonal(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="a", y=1),
                WhitePawn(board=board, team=board.white, x="a", y=2),
                Bishop(board=board, team=board.white, x="b", y=1),
                King(board=board, team=board.black, x="h", y=8),
                Bishop(board=board, team=board.black, x="h", y=6),
            ]
        )

        board.black["B1"].manual_move("g", 7)

        with pytest.raises(InvalidMoveError):
            board.white["K"].manual_move("b", 2)
