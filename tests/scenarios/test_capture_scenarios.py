from main.pieces import Bishop, King, Knight, Queen, Rook


class TestCaptureScenarios:
    def test_capture_removes_piece_from_agent(self, default_board):
        default_board.white.move("d_pawn", "d", 4)
        default_board.black.move("e_pawn", "e", 6)
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("f_bishop", "a", 3)
        default_board.white.move("g_pawn", "g", 3)
        assert ("b", 2) in default_board.white.pieces

        # Black bishop captures B pawn
        default_board.black.move("f_bishop", "b", 2)
        assert default_board.black.f_bishop.position == ("b", 2)
        assert ("b", 2) not in default_board.white.pieces

    def test_capture_puts_captured_piece_in_graveyard(self, builder):
        """
        Aside: There was a weird bug where if a King was within two valid knight moves,
        (as seen here - Nf6 -> Nxe8??) that moving knight would "capture" it due to
        recursive checks for checks, and move applications. We avoid this now by adding
        an "augment" flag to Piece.construct_change, but be on the lookout for other
        similar bugs.
        """

        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Knight, "x": "g", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": Bishop, "x": "e", "y": 5},
                {"piece_type": Rook, "x": "h", "y": 6},
            ],
        )

        board.white.move("g_knight", "h", 6)

        assert board.black.h_rook is None
        assert board.black.graveyard.h_rook
        assert board.black.graveyard.c_bishop is None

    def test_queen_capture_and_check_results_in_expected_change(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Rook, "x": "d", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
                {"piece_type": Queen, "x": "g", "y": 1},
            ],
            active_color="b",
        )
        halfmove = board.black.move("queen", "d", 4)

        assert board.white.graveyard.a_rook
        assert halfmove.change == {
            "WHITE": {
                "a_rook": {
                    "old_position": ("d", 4),
                    "new_position": None,
                },
            },
            "BLACK": {
                "queen": {
                    "old_position": ("g", 1),
                    "new_position": ("d", 4),
                }
            },
            "disambiguation": "",
            "check": True,
            "game_result": None,
            "symbol": "Q",
            "halfmove_clock": (0, 0),
            "fullmove_number": (1, 2),
            "fen": "8/8/8/4k3/2Kq4/8/8/8 w - - 0 2",
        }
