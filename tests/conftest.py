import pytest

from main import constants
from main.agents import ManualAgent
from main.builders import BoardBuilder
from main.game_tree import FullMove, HalfMove
from main.pieces import Queen


@pytest.fixture
def default_board():
    builder = BoardBuilder()
    return builder.from_start(white_agent_cls=ManualAgent, black_agent_cls=ManualAgent)


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
                    },
                ),
                child=FullMove(),
            ),
        ),
    )


@pytest.fixture
def two_fullmove_tree():
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
                },
            ),
            child=FullMove(),
        ),
    )


@pytest.fixture
def one_and_a_half_fullmove_tree():
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
                },
            ),
            black=None,
            child=None,
        ),
    )


@pytest.fixture
def one_fullmove_tree():
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
            },
        ),
        child=FullMove(),
    )


@pytest.fixture
def half_move_tree():
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
                    "K": {
                        "old_position": ("e", 1),
                        "new_position": ("g", 1),
                        "has_moved": True,
                    },
                    "R2": {
                        "old_position": ("h", 1),
                        "new_position": ("f", 1),
                        "has_moved": True,
                    },
                },
                "BLACK": {},
                "disambiguation": "",
                "check": False,
                "game_result": None,
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
                    "Q2": {
                        "old_position": ("h", 4),
                        "new_position": ("e", 1),
                    }
                },
                "BLACK": {
                    "Q1": {
                        "old_position": ("e", 1),
                        "new_position": None,
                    }
                },
                # There are other white queens on both the h-file and 4-rank
                "disambiguation": "h4",
                # Other possible keywords:
                "check": True,
                "game_result": "1-0",
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
                    "GP": {
                        "old_position": ("f", 7),
                        "new_position": None,
                    },
                    "Q2": {
                        "old_position": None,
                        "new_position": ("g", 8),
                        "piece_type": Queen,
                    },
                },
                "BLACK": {
                    "R2": {
                        "old_position": ("g", 8),
                        "new_position": None,
                    }
                },
                "disambiguation": "",
                "check": False,
                "game_result": None,
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
