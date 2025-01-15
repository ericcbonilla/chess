from main.pieces import Bishop, King, Knight, Queen, Rook, WhitePawn


class TestGetGameResult:
    def test_white_in_check_and_cant_move_yields_checkmate(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Queen, "x": "f", "y": 8},
                {"piece_type": Queen, "x": "b", "y": 7},
            ],
            active_color="b",
        )
        halfmove = board.black.move("queen", "a", 8)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] == "0-1"

    def test_white_in_check_and_cant_move_defenders_yields_checkmate(self, builder):
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
        halfmove = board.black.move("c_bishop", "g", 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] == "0-1"

    def test_opponent_not_in_check_and_cant_moves_yields_draw(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 6},
                {"piece_type": Rook, "x": "h", "y": 6},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )
        board.halfmove_clock = 20
        board.fullmove_number = 10
        halfmove = board.white.move("h_rook", "b", 6)

        assert not halfmove.change["check"]
        assert halfmove.change["game_result"] == "½-½ Stalemate"

    def test_opponent_in_check_but_can_still_move_yields_no_result(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": WhitePawn, "x": "a", "y": 2},
                {"piece_type": Knight, "x": "b", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Bishop, "x": "h", "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("c_bishop", "g", 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] is None  # Can still do Nc3

    def test_opponent_in_check_but_pawn_can_still_move_yields_no_result(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": WhitePawn, "x": "a", "y": 2},
                {"piece_type": WhitePawn, "x": "d", "y": 3},
                {"piece_type": Bishop, "x": "b", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Bishop, "x": "h", "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("c_bishop", "g", 7)

        assert halfmove.change["check"]
        assert halfmove.change["game_result"] is None  # Can still do d4


class TestGetDisambiguation:
    def test_knight_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Knight, "x": "c", "y": 3},
                {"piece_type": Knight, "x": "g", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation("e", 4) == "c"

    def test_knight_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Knight, "x": "c", "y": 3},
                {"piece_type": Knight, "x": "g", "y": 3},
                {"piece_type": Knight, "x": "c", "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation("e", 4) == "c3"

    def test_knight_two_knights_but_just_one_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Knight, "x": "c", "y": 3},
                {"piece_type": Knight, "x": "g", "y": 3},
                {"piece_type": Knight, "x": "g", "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.b_knight.get_disambiguation("e", 4) == "c"

    def test_rook_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Rook, "x": "g", "y": 1},
                {"piece_type": Rook, "x": "g", "y": 6},
                {"piece_type": Rook, "x": "c", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.a_rook.get_disambiguation("g", 3) == "1"

    def test_rook_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Rook, "x": "g", "y": 1},
                {"piece_type": Rook, "x": "g", "y": 6},
                {"piece_type": Rook, "x": "c", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.a_rook.get_disambiguation("g", 3) == "g1"

    def test_queen_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Queen, "x": "b", "y": 2},
                {"piece_type": Queen, "x": "b", "y": 4},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.queen.get_disambiguation("d", 4) == "2"

    def test_queen_double_disambiguation(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Queen, "x": "b", "y": 2},
                {"piece_type": Queen, "x": "b", "y": 4},
                {"piece_type": Queen, "x": "f", "y": 6},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.queen.get_disambiguation("d", 4) == "b2"

    def test_hella_siblings_disambiguation(self, builder):
        """
        If we already have the most specific disambiguation possible,
        we don't need to keep looking
        """

        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": Knight, "x": "g", "y": 3},
                {"piece_type": Knight, "x": "c", "y": 5},
                {"piece_type": Knight, "x": "g", "y": 8},
                {"piece_type": Knight, "x": "h", "y": 8},
                {"piece_type": Knight, "x": "c", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
            ],
        )

        assert board.white.c_prom.get_disambiguation("e", 4) == "c3"
