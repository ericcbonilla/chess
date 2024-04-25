from main.board import Board
from main.pieces import Rook, Queen, King, Knight, Bishop, WhitePawn


class TestGetGameResult:
    def test_white_in_check_and_cant_move_yields_checkmate(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),

            King(board=board, team=board.black, x='h', y=8),
            Queen(board=board, team=board.black, x='f', y=8),
            Queen(board=board, team=board.black, x='b', y=7),
        ])

        board.black['Q1'].manual_move('a', 8)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change['check']
        assert halfmove.change['game_result'] == '0-1'

    def test_white_in_check_and_cant_move_defenders_yields_checkmate(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            WhitePawn(board=board, team=board.white, x='a', y=2),
            Bishop(board=board, team=board.white, x='b', y=1),

            King(board=board, team=board.black, x='h', y=8),
            Bishop(board=board, team=board.black, x='h', y=6),
        ])

        board.black['B1'].manual_move('g', 7)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change['check']
        assert halfmove.change['game_result'] == '0-1'

    def test_opponent_not_in_check_and_cant_moves_yields_draw(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=6),
            Rook(board=board, team=board.white, x='h', y=6),

            King(board=board, team=board.black, x='a', y=8),
        ])

        board.white['R1'].manual_move('b', 6)

        halfmove = board.game_tree.get_latest_halfmove()
        assert not halfmove.change['check']
        assert halfmove.change['game_result'] == '½-½'

    def test_opponent_in_check_but_can_still_move_yields_no_result(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='h', y=8),

            WhitePawn(board=board, team=board.white, x='a', y=2),
            Knight(board=board, team=board.white, x='b', y=1),
            Bishop(board=board, team=board.black, x='h', y=6),
        ])

        board.black['B1'].manual_move('g', 7)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change['check']
        # Can still do Nc3
        assert halfmove.change['game_result'] == ''

    def test_opponent_in_check_but_pawn_can_still_move_yields_no_result(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            WhitePawn(board=board, team=board.white, x='a', y=2),
            WhitePawn(board=board, team=board.white, x='d', y=3),
            Bishop(board=board, team=board.white, x='b', y=1),

            King(board=board, team=board.black, x='h', y=8),
            Bishop(board=board, team=board.black, x='h', y=6),
        ])

        board.black['B1'].manual_move('g', 7)

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change['check']
        # Can still do d4
        assert halfmove.change['game_result'] == ''


class TestGetDisambiguation:
    def test_knight_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Knight(board=board, team=board.white, x='c', y=3),
            Knight(board=board, team=board.white, x='g', y=3),
        ])

        assert board.white['N1'].get_disambiguation('e', 4) == 'c'

    def test_knight_double_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Knight(board=board, team=board.white, x='c', y=3),
            Knight(board=board, team=board.white, x='g', y=3),
            Knight(board=board, team=board.white, x='c', y=5),
        ])

        assert board.white['N1'].get_disambiguation('e', 4) == 'c3'

    def test_knight_two_knights_but_just_one_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Knight(board=board, team=board.white, x='c', y=3),
            Knight(board=board, team=board.white, x='g', y=3),
            Knight(board=board, team=board.white, x='g', y=5),
        ])

        assert board.white['N1'].get_disambiguation('e', 4) == 'c'

    def test_rook_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Rook(board=board, team=board.white, x='g', y=1),
            Rook(board=board, team=board.white, x='g', y=6),
            Rook(board=board, team=board.white, x='c', y=4),
        ])

        assert board.white['R1'].get_disambiguation('g', 3) == '1'

    def test_rook_double_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Rook(board=board, team=board.white, x='g', y=1),
            Rook(board=board, team=board.white, x='g', y=6),
            Rook(board=board, team=board.white, x='c', y=3),
        ])

        assert board.white['R1'].get_disambiguation('g', 3) == 'g1'

    def test_queen_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Queen(board=board, team=board.white, x='b', y=2),
            Queen(board=board, team=board.white, x='b', y=4),
        ])

        assert board.white['Q1'].get_disambiguation('d', 4) == '2'

    def test_queen_double_disambiguation(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Queen(board=board, team=board.white, x='b', y=2),
            Queen(board=board, team=board.white, x='b', y=4),
            Queen(board=board, team=board.white, x='f', y=6),
        ])

        assert board.white['Q1'].get_disambiguation('d', 4) == 'b2'

    def test_hella_siblings_disambiguation(self):
        """
        If we already have the most specific disambiguation possible,
        we don't need to keep looking
        """

        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='a', y=1),
            King(board=board, team=board.black, x='a', y=8),

            Knight(board=board, team=board.white, x='g', y=3),
            Knight(board=board, team=board.white, x='c', y=5),
            Knight(board=board, team=board.white, x='g', y=8),
            Knight(board=board, team=board.white, x='h', y=8),
            Knight(board=board, team=board.white, x='c', y=3),
        ])

        assert board.white['N5'].get_disambiguation('e', 4) == 'c3'
