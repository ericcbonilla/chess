from main.board import Board
from main.pieces import Bishop, King, Knight, Queen, Rook


class TestCaptureScenarios:
    def test_capture_removes_piece_from_team(self, default_board):
        default_board.white["DP"].random_move()
        default_board.black["EP"].random_move()
        default_board.white["N2"].random_move()
        default_board.black["B2"].manual_move("a", 3)
        default_board.white["GP"].random_move()
        assert ("b", 2) in default_board.white.positions

        # Black bishop captures B pawn
        default_board.black["B2"].manual_move("b", 2)
        assert default_board.black["B2"].position == ("b", 2)
        assert ("b", 2) not in default_board.white.positions

    def test_capture_puts_captured_piece_in_graveyard(self):
        """
        Aside: There was a weird bug where if a King was within two valid knight moves,
        (as seen here - Nf6 -> Nxe8??) that moving knight would "capture" it due to
        recursive checks for checks, and move applications. We avoid this now by adding
        an "augment" flag to Piece.construct_change, but be on the lookout for other
        similar bugs.
        """

        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="c", y=4),
                King(board=board, team=board.black, x="e", y=8),
                Bishop(board=board, team=board.black, x="e", y=5),
                Knight(board=board, team=board.white, x="g", y=4),
                Rook(board=board, team=board.black, x="h", y=6),
            ]
        )

        board.white["N1"].manual_move("h", 6)

        assert "R1" not in board.black
        assert "R1" in board.black_graveyard
        assert "B1" not in board.black_graveyard

    def test_queen_capture_and_check_results_in_expected_change(self):
        board = Board()
        board.add_pieces(
            [
                King(board=board, team=board.white, x="c", y=4),
                Rook(board=board, team=board.white, x="d", y=4),
                King(board=board, team=board.black, x="e", y=5),
                Queen(board=board, team=board.black, x="g", y=1),
            ]
        )

        board.black["Q1"].manual_move("d", 4)
        halfmove = board.game_tree.get_latest_halfmove()

        assert "R1" in board.white_graveyard
        assert halfmove.change == {
            "WHITE": {
                "R1": {
                    "old_position": ("d", 4),
                    "new_position": None,
                },
            },
            "BLACK": {
                "Q1": {
                    "old_position": ("g", 1),
                    "new_position": ("d", 4),
                }
            },
            "disambiguation": "",
            "check": True,
            "game_result": "",
        }
