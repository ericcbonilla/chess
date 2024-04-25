import pytest

from main.board import Board
from main.exceptions import InvalidMoveError
from main.pieces import BlackPawn, King, Knight, Queen, Rook, WhitePawn


class TestPawnScenarios:
    def test_pawn_can_capture_pawn(self, default_board):
        default_board.white['EP'].manual_move('e', 4)
        default_board.black['DP'].manual_move('d', 5)

        default_board.white['EP'].manual_move('d', 5)

        assert default_board.white['EP'].position == ('d', 5)
        assert 'DP' not in default_board.black
        assert 'DP' in default_board.black_graveyard

    def test_pawn_cannot_capture_forward(self, default_board):
        default_board.white['EP'].manual_move('e', 4)
        default_board.black['EP'].manual_move('e', 5)

        with pytest.raises(InvalidMoveError):
            default_board.white['EP'].manual_move('e', 5)

    def test_pawn_promotion_capture_results_in_expected_state(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='c', y=4),
            King(board=board, team=board.black, x='e', y=5),
            Rook(board=board, team=board.black, x='g', y=8),
            WhitePawn(board=board, team=board.white, x='f', y=7),
        ])

        board.white['FP'].manual_move('g', 8, promotion_type='Q')

        assert 'FP' in board.white_graveyard
        assert 'R1' in board.black_graveyard
        assert board.white['Q1'].position == ('g', 8)

    def test_rollback_pawn_promotion_capture_results_in_expected_state(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='c', y=4),
            King(board=board, team=board.black, x='e', y=5),
            Rook(board=board, team=board.black, x='g', y=8),
            WhitePawn(board=board, team=board.white, x='f', y=7),
        ])

        board.white['FP'].manual_move('g', 8, promotion_type='Q')
        board.rollback_halfmove()

        assert board.white['FP'].position == ('f', 7)
        assert board.black['R1'].position == ('g', 8)
        assert 'Q1' not in board.white
        assert 'Q1' in board.white_graveyard
        assert board.piece_counts['WHITE_QUEENS'] == 0

    def test_pawn_promotion_can_create_third_piece(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='c', y=4),
            King(board=board, team=board.black, x='e', y=5),
            WhitePawn(board=board, team=board.white, x='f', y=7),
            Knight(board=board, team=board.white, x='a', y=1),
            Knight(board=board, team=board.white, x='b', y=1),
        ])

        board.white['FP'].manual_move('f', 8, promotion_type='N')

        assert board.white['N3'].position == ('f', 8)

    def test_pawn_promotion_capture_results_in_expected_piece(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='c', y=4),
            King(board=board, team=board.black, x='e', y=5),
            WhitePawn(board=board, team=board.white, x='f', y=7),
            Rook(board=board, team=board.black, x='g', y=8),
        ])

        board.white['FP'].manual_move('g', 8, promotion_type='N')

        assert board.white['N1'].position == ('g', 8)
        assert 'R1' in board.black_graveyard

    def test_pawn_promotion_invalid_if_king_is_in_check(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='h', y=7),
            King(board=board, team=board.black, x='e', y=5),
            WhitePawn(board=board, team=board.white, x='f', y=7),
            Queen(board=board, team=board.black, x='a', y=7),
        ])

        with pytest.raises(InvalidMoveError):
            board.white['FP'].manual_move('f', 8, promotion_type='Q')

        # Also check that the pawn is left unchanged - we want to ensure
        # the king_is_in_check method has no side effects
        assert board.white['FP'].position == ('f', 7)
        assert 'Q1' not in board.white

    def test_pawn_promotion_capture_results_in_expected_change(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='c', y=4),
            King(board=board, team=board.black, x='e', y=5),
            Rook(board=board, team=board.black, x='g', y=8),
            WhitePawn(board=board, team=board.white, x='f', y=7),
        ])

        board.white['FP'].manual_move('g', 8, promotion_type='Q')

        halfmove = board.game_tree.get_latest_halfmove()
        assert halfmove.change == {
            'WHITE': {
                'FP': {
                    'old_position': ('f', 7),
                    'new_position': None,
                },
                'Q1': {
                    'old_position': None,
                    'new_position': ('g', 8),
                    'piece_type': Queen,
                }
            },
            'BLACK': {
                'R1': {
                    'old_position': ('g', 8),
                    'new_position': None,
                }
            },
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }


class TestEnPassant:
    def test_white_pawn_moving_two_squares_sets_en_passant_target(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='e', y=1),
            WhitePawn(board=board, team=board.white, x='e', y=2),
            King(board=board, team=board.black, x='e', y=8),
        ])

        board.white['EP'].manual_move('e', 4)

        assert board.white.en_passant_target == ('e', 3)

    def test_black_pawn_moving_two_squares_sets_en_passant_target(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='e', y=1),
            King(board=board, team=board.black, x='e', y=8),
            BlackPawn(board=board, team=board.black, x='d', y=7),
        ])

        board.black['DP'].manual_move('d', 5)

        assert board.black.en_passant_target == ('d', 6)

    def test__pawn_moving_one_square_does_not_set_en_passant_target(self):
        board = Board()
        board.add_pieces([
            King(board=board, team=board.white, x='e', y=1),
            WhitePawn(board=board, team=board.white, x='e', y=2),
            King(board=board, team=board.black, x='e', y=8),
        ])

        board.white['EP'].manual_move('e', 3)

        assert board.white.en_passant_target is None

    def test_pawn_cannot_capture_en_passant_if_target_has_expired(self, default_board):
        default_board.white['DP'].manual_move('d', 4)
        default_board.black['GP'].manual_move('g', 6)
        default_board.white['DP'].manual_move('d', 5)
        default_board.black['EP'].manual_move('e', 5)

        assert default_board.black.en_passant_target == ('e', 6)

        # Waiting move
        default_board.white['Q1'].manual_move('d', 2)
        default_board.black['GP'].manual_move('g', 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white['DP'].manual_move('e', 6)

    def test_pawn_cannot_capture_en_passant_if_target_did_not_advance_two_squares(self, default_board):
        default_board.white['DP'].manual_move('d', 4)
        default_board.black['GP'].manual_move('g', 6)
        default_board.white['DP'].manual_move('d', 5)
        default_board.black['EP'].manual_move('e', 6)

        # Waiting move
        default_board.white['Q1'].manual_move('d', 2)
        default_board.black['EP'].manual_move('e', 5)

        assert default_board.black.en_passant_target is None

        with pytest.raises(InvalidMoveError):
            default_board.white['DP'].manual_move('e', 6)

    def test_capturing_en_passant_results_in_expected_state(self, default_board):
        default_board.white['DP'].manual_move('d', 4)
        default_board.black['GP'].manual_move('g', 6)
        default_board.white['DP'].manual_move('d', 5)
        default_board.black['EP'].manual_move('e', 5)

        # En passant
        default_board.white['DP'].manual_move('e', 6)

        assert default_board.white['DP'].position == ('e', 6)
        assert 'EP' in default_board.black_graveyard
        assert default_board.black.en_passant_target is None

        halfmove = default_board.game_tree.get_latest_halfmove()
        assert halfmove.change == {
            'WHITE': {
                'DP': {
                    'old_position': ('d', 5),
                    'new_position': ('e', 6),
                },
            },
            'BLACK': {
                'en_passant_target': (('e', 6), None),
                'EP': {
                    'old_position': ('e', 5),
                    'new_position': None,
                }
            },
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }

    def test_rollback_en_passant_results_in_expected_state(self, default_board):
        default_board.white['DP'].manual_move('d', 4)
        default_board.black['GP'].manual_move('g', 6)
        default_board.white['DP'].manual_move('d', 5)
        default_board.black['EP'].manual_move('e', 5)

        # En passant
        default_board.white['DP'].manual_move('e', 6)
        default_board.rollback_halfmove()

        assert default_board.white['DP'].position == ('d', 5)
        assert default_board.black['EP'].position == ('e', 5)
        assert default_board.black.en_passant_target == ('e', 6)
