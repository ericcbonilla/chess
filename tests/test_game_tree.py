import pytest

from main import constants
from main.game_tree import FullMove, GameTree, HalfMove
from main.game_tree.utils import get_halfmove
from main.pieces import King, Knight, Queen, Rook, WhitePawn


class TestGetLatestHalfmove:
    def test_get_latest_halfmove_returns_first_move(self, half_move_root):
        tree = GameTree.backfill(root=half_move_root)
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
                "caches": {},
                "registry": ({}, {}),
            },
        )

        assert tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_second_move(self, one_fullmove_root):
        tree = GameTree.backfill(root=one_fullmove_root)
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
                "caches": {},
                "registry": ({}, {}),
            },
        )

        assert tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_third_move(self, one_and_a_half_fullmove_root):
        tree = GameTree.backfill(root=one_and_a_half_fullmove_root)
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
                "caches": {},
                "registry": ({}, {}),
            },
        )

        assert tree.get_latest_halfmove() == expected

    def test_get_latest_halfmove_returns_fourth_move(self, two_fullmove_root):
        tree = GameTree.backfill(root=two_fullmove_root)
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
                "caches": {},
                "registry": ({}, {}),
            },
        )

        assert tree.get_latest_halfmove() == expected


class TestGameTreeMutations:
    def test_append_white_move_results_in_expected_tree(self, empty_change):
        tree = GameTree()
        tree.append(HalfMove(color=constants.WHITE, change=empty_change))

        assert tree.root == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
            child=None,
        )
        assert tree.latest_fullmove is tree.root
        assert tree.second_latest_fullmove is None
        assert tree.third_latest_fullmove is None

    def test_append_black_move_results_in_expected_tree(self, empty_change):
        tree = GameTree()
        tree.append(HalfMove(color=constants.WHITE, change=empty_change))
        tree.append(HalfMove(color=constants.BLACK, change=empty_change))

        assert tree.root == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(),
        )
        assert tree.latest_fullmove == FullMove()
        assert tree.second_latest_fullmove is tree.root
        assert tree.third_latest_fullmove is None

    def test_remove_first_move_results_in_expected_tree(self, empty_change):
        tree = GameTree()
        tree.append(HalfMove(color=constants.WHITE, change=empty_change))

        tree.prune()

        assert tree.root == FullMove()
        assert tree.latest_fullmove is tree.root

    def test_remove_second_move_results_in_expected_tree(self, empty_change):
        tree = GameTree()
        tree.append(HalfMove(color=constants.WHITE, change=empty_change))
        tree.append(HalfMove(color=constants.BLACK, change=empty_change))
        tree.prune()

        assert tree.root == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=None,
            child=None,
        )
        assert tree.latest_fullmove is tree.root
        assert tree.second_latest_fullmove is None
        assert tree.third_latest_fullmove is None

    def test_remove_black_move_results_in_expected_tree(self, empty_change):
        tree = GameTree.backfill(
            root=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=HalfMove(color=constants.BLACK, change=empty_change),
                child=FullMove(
                    white=HalfMove(color=constants.WHITE, change=empty_change),
                    black=HalfMove(color=constants.BLACK, change=empty_change),
                    child=FullMove(),
                ),
            )
        )

        tree.prune()
        assert tree.root == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=None,
                child=None,
            ),
        )
        assert tree.second_latest_fullmove is tree.root
        assert tree.latest_fullmove is tree.root.child

    def test_remove_white_move_results_in_expected_tree(self, empty_change):
        tree = GameTree.backfill(
            root=FullMove(
                white=HalfMove(color=constants.WHITE, change=empty_change),
                black=HalfMove(color=constants.BLACK, change=empty_change),
                child=FullMove(
                    white=HalfMove(color=constants.WHITE, change=empty_change),
                    black=None,
                    child=None,
                ),
            )
        )
        tree.prune()

        assert tree.root == FullMove(
            white=HalfMove(color=constants.WHITE, change=empty_change),
            black=HalfMove(color=constants.BLACK, change=empty_change),
            child=FullMove(),
        )
        assert tree.second_latest_fullmove is tree.root
        assert tree.latest_fullmove == FullMove()


class TestUtils:
    def test_when_get_halfmove_called_out_of_range_raises_error(self, default_board):
        with pytest.raises(Exception):
            get_halfmove(1, default_board.game_tree)


class TestHalfMove:
    def test_when_piece_moves_to_an_returns_expected(self, default_board):
        halfmove = default_board.white.move("g_knight", "f", 3)
        assert halfmove.to_an() == "Nf3"

    def test_when_pawn_moves_to_an_returns_expected(self, default_board):
        default_board.white.move("e_pawn", "e", 4)
        halfmove = default_board.black.move("c_pawn", "c", 5)
        assert halfmove.to_an() == "c5"

    def test_when_piece_captures_to_an_returns_expected(self, default_board):
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("e_pawn", "e", 5)
        halfmove = default_board.white.move("g_knight", "e", 5)

        assert halfmove.to_an() == "Nxe5"

    def test_when_pawn_captures_to_an_returns_expected(self, default_board):
        default_board.white.move("g_knight", "f", 3)
        default_board.black.move("d_pawn", "d", 6)
        default_board.white.move("g_knight", "e", 5)
        halfmove = default_board.black.move("d_pawn", "e", 5)

        assert halfmove.to_an() == "dxe5"

    def test_when_ambiguous_move_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Queen, "x": "f", "y": 6},
                {"piece_type": Queen, "x": "f", "y": 4},
                {"piece_type": Queen, "x": "h", "y": 6},
            ],
            active_color="b",
        )
        halfmove = board.black.move("queen", "h", 4)

        assert halfmove.to_an() == "Qf6h4"

    def test_when_check_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
                {"piece_type": Queen, "x": "f", "y": 6},
            ],
            active_color="b",
        )

        halfmove = board.black.move("queen", "a", 1)

        assert halfmove.to_an() == "Qa1+"

    def test_when_queenside_castle_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "a", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "h", "y": 8},
            ],
        )
        halfmove = board.white.move("king", "c", 1)

        assert halfmove.to_an() == "O-O-O"

    def test_when_castle_and_check_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "f", "y": 8},
            ],
        )
        halfmove = board.white.move("king", "g", 1)

        assert halfmove.to_an() == "O-O+"

    def test_when_pawn_promotion_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 7},
            ],
        )
        halfmove = board.white.move("e_pawn", "e", 8)

        assert halfmove.to_an() == "e8=Q"

    def test_when_pawn_promotion_capture_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "e", "y": 1},
                {"piece_type": WhitePawn, "x": "e", "y": 7},
            ],
            black_data=[
                {"piece_type": King, "x": "a", "y": 8},
                {"piece_type": Rook, "x": "d", "y": 8},
            ],
        )
        halfmove = board.white.move("e_pawn", "d", 8)

        assert halfmove.to_an() == "exd8=Q+"

    def test_when_checkmate_to_an_returns_expected(self, builder):
        board = builder.from_data(
            white_data=[
                {"piece_type": King, "x": "a", "y": 1},
            ],
            black_data=[
                {"piece_type": King, "x": "c", "y": 1},
                {"piece_type": Rook, "x": "h", "y": 2},
                {"piece_type": Knight, "x": "c", "y": 5},
            ],
            active_color="b",
        )
        halfmove = board.black.move("b_knight", "b", 3)

        assert halfmove.to_an() == "Nb3#"
