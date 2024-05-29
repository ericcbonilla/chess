import pytest

from main import constants
from main.game_tree import FullMove, HalfMove
from main.game_tree.utils import get_halfmove


class TestGetLatestHalfmove:
    def test_get_latest_halfmove_returns_first_move(self, half_move_tree):
        expected = HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "e_pawn": {
                        "old_position": ("e", 2),
                        "new_position": ("e", 4),
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "",
                "halfmove_clock": (0, 0),
                "fullmove_number": (1, 1),
                "fen": "",
            },
        )

        assert half_move_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_second_move(self, one_fullmove_tree):
        expected = HalfMove(
            color=constants.BLACK,
            change={
                "WHITE": {},
                "BLACK": {
                    "e_pawn": {
                        "old_position": ("e", 7),
                        "new_position": ("e", 5),
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "",
                "halfmove_clock": (0, 0),
                "fullmove_number": (1, 2),
                "fen": "",
            },
        )

        assert one_fullmove_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_third_move(self, one_and_a_half_fullmove_tree):
        expected = HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "g_knight": {
                        "old_position": ("g", 1),
                        "new_position": ("f", 3),
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "N",
                "halfmove_clock": (0, 1),
                "fullmove_number": (2, 2),
                "fen": "",
            },
        )

        assert one_and_a_half_fullmove_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_fourth_move(self, two_fullmove_tree):
        expected = HalfMove(
            color=constants.BLACK,
            change={
                "WHITE": {},
                "BLACK": {
                    "b_knight": {
                        "old_position": ("b", 8),
                        "new_position": ("c", 6),
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "N",
                "halfmove_clock": (1, 2),
                "fullmove_number": (2, 3),
                "fen": "",
            },
        )

        assert two_fullmove_tree.get_latest_halfmove() == expected


class TestGameTreeMutations:
    def test_append_white_move_results_in_expected_tree(self, empty_change):
        tree = FullMove()
        white_move = HalfMove(color=constants.WHITE, change=empty_change)
        tree.append(white_move)

        assert tree == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
            child=None,
        )

    def test_append_black_move_results_in_expected_tree(self, empty_change):
        tree = FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
        )
        black_move = HalfMove(color=constants.BLACK, change=empty_change)
        tree.append(black_move)

        assert tree == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(),
        )

    def test_remove_first_move_results_in_expected_tree(self, empty_change):
        tree = FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
            child=None,
        )
        tree.prune()

        assert tree == FullMove()

    def test_remove_second_move_results_in_expected_tree(self, empty_change):
        tree = FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(),
        )
        tree.prune()

        assert tree == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
            child=None,
        )

    def test_remove_black_move_results_in_expected_tree(self, empty_change):
        tree = FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=HalfMove(color=constants.BLACK, change=empty_change),
                child=FullMove(),
            ),
        )
        tree.prune()

        assert tree == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=None,
                child=None,
            ),
        )

    def test_remove_white_move_results_in_expected_tree(self, empty_change):
        tree = FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=None,
                child=None,
            ),
        )
        tree.prune()

        assert tree == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(),
        )


class TestUtils:
    def test_when_get_halfmove_called_out_of_range_raises_error(self, default_board):
        with pytest.raises(Exception):
            get_halfmove(1, default_board.game_tree)
