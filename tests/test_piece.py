from main.pieces import Bishop, King, Knight, Queen, Rook, WhitePawn
from main.x import A, B, C, D, E, F, G, H


class TestGetGameResult:
    def test_white_in_check_and_cant_move_yields_checkmate(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": H, "y": 8},
                {"piece_type": Queen, "x": F, "y": 8},
                {"piece_type": Queen, "x": B, "y": 7},
            ],
            active_color="b",
        )
        halfmove = board.black.move("queen", A, 8)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] == "0-1"

    def test_white_in_check_and_cant_move_defenders_yields_checkmate(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
                {"piece_type": Bishop, "x": B, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": H, "y": 8},
                {"piece_type": Bishop, "x": H, "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("c_bishop", G, 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] == "0-1"

    def test_opponent_not_in_check_and_cant_moves_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 6},
                {"piece_type": Rook, "x": H, "y": 6},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )
        board.halfmove_clock = 20
        board.fullmove_number = 10
        halfmove = board.white.move("h_rook", B, 6)

        assert not halfmove.change["check"]
        assert halfmove.change["game_result"] == "½-½ Stalemate"

    def test_opponent_in_check_but_can_still_move_yields_no_result(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
                {"piece_type": Knight, "x": B, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": H, "y": 8},
                {"piece_type": Bishop, "x": H, "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("c_bishop", G, 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] is None  # Can still do Nc3

    def test_opponent_in_check_but_can_still_capture_pawn_yields_no_result(
        self, builder
    ):
        board = builder.from_fen(
            text="8/p3p1bp/p3B3/2PPk2p/4P2P/K1P5/P7/5RN1 w - - 1 28"
        )
        halfmove = board.white.move("a_rook", F, 5)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] is None  # Can still do Kxe4

    def test_opponent_in_check_but_pawn_can_still_move_yields_no_result(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": WhitePawn, "x": A, "y": 2},
                {"piece_type": WhitePawn, "x": D, "y": 3},
                {"piece_type": Bishop, "x": B, "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": H, "y": 8},
                {"piece_type": Bishop, "x": H, "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("c_bishop", G, 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] is None  # Can still do d4


class TestGetDisambiguation:
    def test_knight_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Knight, "x": C, "y": 3},
                {"piece_type": Knight, "x": G, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation(E, 4) == "c"

    def test_knight_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Knight, "x": C, "y": 3},
                {"piece_type": Knight, "x": G, "y": 3},
                {"piece_type": Knight, "x": C, "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation(E, 4) == "c3"

    def test_knight_two_knights_but_just_one_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Knight, "x": C, "y": 3},
                {"piece_type": Knight, "x": G, "y": 3},
                {"piece_type": Knight, "x": G, "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation(E, 4) == "c"

    def test_rook_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Rook, "x": G, "y": 1},
                {"piece_type": Rook, "x": G, "y": 6},
                {"piece_type": Rook, "x": C, "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.a_rook.get_disambiguation(G, 3) == "1"

    def test_rook_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Rook, "x": G, "y": 1},
                {"piece_type": Rook, "x": G, "y": 6},
                {"piece_type": Rook, "x": C, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.a_rook.get_disambiguation(G, 3) == "g1"

    def test_queen_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Queen, "x": B, "y": 2},
                {"piece_type": Queen, "x": B, "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.queen.get_disambiguation(D, 4) == "2"

    def test_queen_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Queen, "x": B, "y": 2},
                {"piece_type": Queen, "x": B, "y": 4},
                {"piece_type": Queen, "x": F, "y": 6},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.queen.get_disambiguation(D, 4) == "b2"

    def test_hella_siblings_disambiguation(self, builder):
        """
        If we already have the most specific disambiguation possible,
        we don't need to keep looking
        """

        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": A, "y": 1},
                {"piece_type": Knight, "x": G, "y": 3},
                {"piece_type": Knight, "x": C, "y": 5},
                {"piece_type": Knight, "x": G, "y": 8},
                {"piece_type": Knight, "x": H, "y": 8},
                {"piece_type": Knight, "x": C, "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": A, "y": 8},
            ],
        )

        assert board.white.c_prom.get_disambiguation(E, 4) == "c3"
