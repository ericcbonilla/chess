import pytest

from main import constants
from main.builders import BoardBuilder
from main.game_tree import FullMove, HalfMove
from main.pieces import Queen


@pytest.fixture(scope="session")
def builder():
    return BoardBuilder()


@pytest.fixture
def default_board(builder):
    return builder.from_start()


@pytest.fixture
def three_fullmove_tree():
    """
    1. e4 d5
    2. Nf3 Nc6
    3. Bb5 a6
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=HalfMove(
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
            },
        ),
        child=FullMove(
            white=HalfMove(
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
                },
            ),
            black=HalfMove(
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
                },
            ),
            child=FullMove(
                white=HalfMove(
                    color=constants.WHITE,
                    change={
                        "WHITE": {
                            "f_bishop": {
                                "old_position": ("f", 1),
                                "new_position": ("b", 5),
                            },
                        },
                        "BLACK": {},
                        "disambiguation": "",
                        "check": False,
                        "game_result": None,
                        "symbol": "B",
                        "halfmove_clock": (2, 3),
                        "fullmove_number": (3, 3),
                        "fen": "",
                        "caches": {},
                    },
                ),
                black=HalfMove(
                    color=constants.BLACK,
                    change={
                        "WHITE": {},
                        "BLACK": {
                            "a_pawn": {
                                "old_position": ("a", 7),
                                "new_position": ("a", 6),
                            }
                        },
                        "disambiguation": "",
                        "check": False,
                        "game_result": None,
                        "symbol": "",
                        "halfmove_clock": (3, 0),
                        "fullmove_number": (3, 4),
                        "fen": "",
                        "caches": {},
                    },
                ),
                child=FullMove(),
            ),
        ),
    )


@pytest.fixture
def two_fullmove_root():
    """
    1. e4 d5
    2. Nf3 Nc6
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=HalfMove(
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
            },
        ),
        child=FullMove(
            white=HalfMove(
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
                },
            ),
            black=HalfMove(
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
                },
            ),
            child=FullMove(),
        ),
    )


@pytest.fixture
def one_and_a_half_fullmove_root():
    """
    1. e4 d5
    2. Nf3
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=HalfMove(
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
            },
        ),
        child=FullMove(
            white=HalfMove(
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
                },
            ),
            black=None,
            child=None,
        ),
    )


@pytest.fixture
def one_fullmove_root():
    """
    1. e4 d5
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=HalfMove(
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
            },
        ),
        child=FullMove(),
    )


@pytest.fixture
def half_move_root():
    """
    1. e4
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def one_fullmove_then_capture_tree():
    """
    1. e4 d5
    2. exd5
    """

    return FullMove(
        white=HalfMove(
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
            },
        ),
        black=HalfMove(
            color=constants.BLACK,
            change={
                "WHITE": {},
                "BLACK": {
                    "d_pawn": {
                        "old_position": ("d", 7),
                        "new_position": ("d", 5),
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
            },
        ),
        child=FullMove(
            white=HalfMove(
                color=constants.WHITE,
                change={
                    "WHITE": {
                        "e_pawn": {
                            "old_position": ("e", 4),
                            "new_position": ("d", 5),
                        },
                    },
                    "BLACK": {
                        "d_pawn": {
                            "old_position": ("d", 5),
                            "new_position": None,
                        }
                    },
                    "disambiguation": "",
                    "check": False,
                    "game_result": None,
                    "symbol": "",
                    "halfmove_clock": (0, 0),
                    "fullmove_number": (2, 2),
                    "fen": "",
                    "caches": {},
                },
            ),
            black=None,
            child=None,
        ),
    )


@pytest.fixture
def white_kingside_castle():
    # 0-0

    return FullMove(
        white=HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "king": {
                        "old_position": ("e", 1),
                        "new_position": ("g", 1),
                        "has_moved": True,
                    },
                    "h_rook": {
                        "old_position": ("h", 1),
                        "new_position": ("f", 1),
                        "has_moved": True,
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "K",
                "halfmove_clock": (0, 1),
                "fullmove_number": (1, 1),
                "fen": "",
                "caches": {},
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def white_queen_ambiguous_capture():
    return FullMove(
        white=HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "queen": {
                        "old_position": ("h", 4),
                        "new_position": ("e", 1),
                    }
                },
                "BLACK": {
                    "queen": {
                        "old_position": ("e", 1),
                        "new_position": None,
                    }
                },
                # There are other white queens on both the h-file and 4-rank
                "disambiguation": "h4",
                # Other possible keywords:
                "check": True,
                "game_result": "1-0",
                "symbol": "Q",
                "halfmove_clock": (0, 0),
                "fullmove_number": (1, 1),
                "fen": "",
                "caches": {},
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def white_pawn_promotion_to_queen():
    # fxg8=Q

    return FullMove(
        white=HalfMove(
            color=constants.WHITE,
            change={
                "WHITE": {
                    "g_pawn": {
                        "old_position": ("f", 7),
                        "new_position": None,
                    },
                    "g_prom": {
                        "old_position": None,
                        "new_position": ("g", 8),
                        "piece_type": Queen,
                    },
                },
                "BLACK": {
                    "h_rook": {
                        "old_position": ("g", 8),
                        "new_position": None,
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": None,
                "symbol": "",
                "halfmove_clock": (0, 0),
                "fullmove_number": (1, 1),
                "fen": "",
                "caches": {},
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def empty_change():
    return {
        "WHITE": {},
        "BLACK": {},
        "disambiguation": "",
        "check": False,
        "game_result": None,
    }
