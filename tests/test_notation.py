import pytest

from main.exceptions import NotationError
from main.notation import AN, FEN
from main.pieces import Bishop, King, Knight, Pawn, Queen


class TestFEN:
    def test_fen_parser_returns_expected_properties(self):
        fen = FEN(text="rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")

        assert fen.piece_placement == "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR"
        assert fen.active_color == "b"
        assert fen.castling_rights == {
            ("a", 8): True,
            ("h", 8): True,
            ("a", 1): True,
            ("h", 1): True,
            ("e", 8): True,
            ("e", 1): True,
        }
        assert fen.en_passant_target == ("d", 3)
        assert fen.halfmove_clock == 0
        assert fen.fullmove_number == 1


class TestAN:
    def test_pawn_movement_returns_expected_properties(self):
        an = AN(text="d4")

        assert an.piece_type is Pawn
        assert not an.is_capture
        assert an.pick == ("d", 4)

    def test_pawn_capture_returns_expected_properties(self):
        an = AN(text="exd5")

        assert an.piece_type is Pawn
        assert an.pawn_file == "e"
        assert an.is_capture
        assert an.pick == ("d", 5)

    def test_piece_movement_returns_expected_properties(self):
        an = AN(text="Nc3")

        assert an.piece_type is Knight
        assert an.pawn_file is None
        assert not an.is_capture
        assert an.pick == ("c", 3)

    def test_piece_capture_returns_expected_properties(self):
        an = AN(text="Bxg5")

        assert an.piece_type is Bishop
        assert an.is_capture
        assert an.pick == ("g", 5)

    def test_disamb_rank_returns_expected_properties(self):
        an = AN(text="Q4e1+")

        assert an.piece_type is Queen
        assert an.disambiguation == 4

    def test_disamb_file_returns_expected_properties(self):
        an = AN(text="Qae1+")

        assert an.piece_type is Queen
        assert an.disambiguation == "a"

    def test_double_disamb_returns_expected_properties(self):
        an = AN(text="Qh4e1+")

        assert an.piece_type is Queen
        assert an.disambiguation == ("h", 4)

    def test_promotion_returns_expected_properties(self):
        an = AN(text="exd8=N+")

        assert an.pawn_file == "e"
        assert an.pick == ("d", 8)
        assert an.promotee_type is Knight

    def test_check_returns_expected_properties(self):
        an = AN(text="Qae1+")

        assert an.check
        assert not an.checkmate

    def test_checkmate_returns_expected_properties(self):
        an = AN(text="Qae1#")

        assert an.check
        assert an.checkmate

    def test_kingside_castle_returns_expected_properties(self):
        an = AN(text="O-O")

        assert an.piece_type is King
        assert an.pawn_file is None
        assert an.disambiguation is None
        assert not an.is_capture
        assert an.x == "g"
        assert an.y is None
        assert an.promotee_type is None
        assert not an.check
        assert not an.checkmate

    def test_queenside_castle_check_returns_expected_properties(self):
        an = AN(text="O-O-O+")

        assert an.x == "c"
        assert an.check

    def test_invalid_an_passed_raises_notation_error(self):
        with pytest.raises(NotationError):
            AN(text="Deez")

    def test_pawns_are_not_erroneously_ambiguated(self, default_board):
        default_board.white.move(an_text="a4")
        default_board.black.move(an_text="h6")

        # It was erroneously saying the a4 pawn could also move to b3, and asking
        # for a disambiguation
        default_board.white.move(an_text="b3")

        assert default_board.white.b_pawn.position == ("b", 3)
