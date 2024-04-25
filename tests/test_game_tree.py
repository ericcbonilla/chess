from main import constants
from main.game_tree import FullMove, HalfMove


class TestGetLatestHalfmove:
    def test_get_latest_halfmove_returns_first_move(self, half_move_tree):
        expected = HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "EP": {
                        "old_position": ("e", 2),
                        "new_position": ("e", 4),
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": "",
            },
        )

        assert half_move_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_second_move(self, one_fullmove_tree):
        expected = HalfMove(
            color=constants.BLACK,
            change={
                "WHITE": {},
                "BLACK": {
                    "EP": {
                        "old_position": ("e", 7),
                        "new_position": ("e", 5),
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": "",
            },
        )

        assert one_fullmove_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_third_move(self, one_and_a_half_fullmove_tree):
        expected = HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "N2": {
                        "old_position": ("g", 1),
                        "new_position": ("f", 3),
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": "",
            },
        )

        assert one_and_a_half_fullmove_tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_fourth_move(self, two_fullmove_tree):
        expected = HalfMove(
            color=constants.BLACK,
            change={
                "WHITE": {},
                "BLACK": {
                    "N1": {
                        "old_position": ("b", 8),
                        "new_position": ("c", 6),
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": "",
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
