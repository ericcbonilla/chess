import pytest

from main.agents import AggressiveAgent
from main.exceptions import GameplayError
from main.pieces import BlackPawn, King, Knight, Queen, Rook, WhitePawn


class TestManualAgent:
    def test_when_moving_with_an_piece_moves_as_expected(self, default_board):
        default_board.white.move(an_text="Nc3")

        assert default_board.white.b_knight.position == ("c", 3)

    def test_when_capturing_with_an_piece_captures_as_expected(self, default_board):
        default_board.white.move(an_text="d4")
        default_board.black.move(an_text="e5")
        default_board.white.move(an_text="dxe5")

        assert default_board.white.d_pawn.position == ("e", 5)
        assert default_board.black.graveyard.e_pawn

    def test_when_capturing_with_an_x_required(self, default_board, capsys):
        default_board.white.move(an_text="Nc3")
        default_board.black.move(an_text="Nf6")
        default_board.white.move(an_text="Ne4")

        try:
            default_board.black.move(an_text="Ne4")
        except OSError:
            pass

        captured = capsys.readouterr()
        assert "Opponent piece on e4. Did you mean Nxe4?" in captured.out

    def test_when_moving_ambiguous_piece_requires_disambiguation(self, builder, capsys):
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

        try:
            board.white.move(an_text="Rg3")
        except OSError:
            pass

        captured = capsys.readouterr()
        assert (
            "More than one Rook can move to g3; disambiguation required" in captured.out
        )

        board.white.move(an_text="Rg1g3")
        assert board.white.a_rook.position == ("g", 3)

    def test_when_castling_with_an_pieces_move_as_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "a", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        board.white.move(an_text="O-O")
        assert board.white.king.position == ("g", 1)
        assert board.white.h_rook.position == ("f", 1)

    def test_when_promoting_with_an_pieces_move_as_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "a", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        board.white.move(an_text="a8=N")
        assert board.white.a_prom.position == ("a", 8)
        assert isinstance(board.white.a_prom, Knight)

    def test_when_promoting_with_an_requires_valid_symbol(self, builder, capsys):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "a", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
            ],
        )

        try:
            board.white.move(an_text="a8=Deez")
        except OSError:
            pass

        captured = capsys.readouterr()
        assert "Invalid promotee value, must be one of B, N, R, or Q" in captured.out

    def test_when_move_is_valid_an_but_illegal_requires_legal_move(
        self, default_board, capsys
    ):
        try:
            default_board.white.move(an_text="Nd2")
        except OSError:
            pass

        captured = capsys.readouterr()
        assert '"Nd2" is an illegal move' in captured.out

    def test_agent_cant_move_when_not_active(self, default_board):
        with pytest.raises(GameplayError) as exc_info:
            default_board.black.move("e_pawn", "e", 5)

        assert str(exc_info.value) == "Agent is not active"

    def test_agent_cant_move_when_game_has_ended(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "d", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 4},
            ],
            active_color="b",
        )
        board.black.move("king", "d", 3)

        with pytest.raises(GameplayError) as exc_info:
            board.white.move("king", "f", 1)

        assert str(exc_info.value) == "The game has ended"


class TestAggressiveAgent:
    def test_pawn_captures_when_available(self, builder):
        board = builder.from_data(
            white_agent_cls=AggressiveAgent,
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": BlackPawn, "x": "f", "y": 6},
                {"piece_type": Queen, "x": "c", "y": 2},
            ],
        )

        halfmove = board.white.move()
        assert halfmove.to_an() == "exf6"

    def test_pawn_captures_when_only_move(self, builder):
        board = builder.from_data(
            white_agent_cls=AggressiveAgent,
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 5},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 8},
                {"piece_type": BlackPawn, "x": "f", "y": 6},
                {"piece_type": BlackPawn, "x": "e", "y": 6},
                {"piece_type": Queen, "x": "c", "y": 2},
            ],
        )

        halfmove = board.white.move()
        assert halfmove.to_an() == "exf6"
