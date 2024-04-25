import pytest

from main import constants
from main.board import Board
from main.game_tree import FullMove, HalfMove
from main.pieces import Bishop, BlackPawn, King, Knight, Queen, Rook, WhitePawn


@pytest.fixture
def default_board():
    board = Board()
    board.add_pieces([
        WhitePawn(board=board, team=board.white, x='a', y=2),
        WhitePawn(board=board, team=board.white, x='b', y=2),
        WhitePawn(board=board, team=board.white, x='c', y=2),
        WhitePawn(board=board, team=board.white, x='d', y=2),
        WhitePawn(board=board, team=board.white, x='e', y=2),
        WhitePawn(board=board, team=board.white, x='f', y=2),
        WhitePawn(board=board, team=board.white, x='g', y=2),
        WhitePawn(board=board, team=board.white, x='h', y=2),
        Rook(board=board, team=board.white, x='a', y=1),
        Rook(board=board, team=board.white, x='h', y=1),
        Knight(board=board, team=board.white, x='b', y=1),
        Knight(board=board, team=board.white, x='g', y=1),
        Bishop(board=board, team=board.white, x='c', y=1),
        Bishop(board=board, team=board.white, x='f', y=1),
        Queen(board=board, team=board.white, x='d', y=1),
        King(board=board, team=board.white, x='e', y=1),

        BlackPawn(board=board, team=board.black, x='a', y=7),
        BlackPawn(board=board, team=board.black, x='b', y=7),
        BlackPawn(board=board, team=board.black, x='c', y=7),
        BlackPawn(board=board, team=board.black, x='d', y=7),
        BlackPawn(board=board, team=board.black, x='e', y=7),
        BlackPawn(board=board, team=board.black, x='f', y=7),
        BlackPawn(board=board, team=board.black, x='g', y=7),
        BlackPawn(board=board, team=board.black, x='h', y=7),
        Rook(board=board, team=board.black, x='a', y=8),
        Rook(board=board, team=board.black, x='h', y=8),
        Knight(board=board, team=board.black, x='b', y=8),
        Knight(board=board, team=board.black, x='g', y=8),
        Bishop(board=board, team=board.black, x='c', y=8),
        Bishop(board=board, team=board.black, x='f', y=8),
        Queen(board=board, team=board.black, x='d', y=8),
        King(board=board, team=board.black, x='e', y=8),
    ])

    return board


@pytest.fixture
def three_fullmove_tree():
    """
    1. e4 d5
    2. Nf3 Nc6
    3. Bb5 a6
    """

    return FullMove(
        white=HalfMove(color=constants.WHITE, change={
            'WHITE': {
                'EP': {
                    'old_position': ('e', 2),
                    'new_position': ('e', 4),
                },
            },
            'BLACK': {},
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }),
        black=HalfMove(color=constants.BLACK, change={
            'WHITE': {},
            'BLACK': {
                'EP': {
                    'old_position': ('e', 7),
                    'new_position': ('e', 5),
                }
            },
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }),
        child=FullMove(
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'N2': {
                        'old_position': ('g', 1),
                        'new_position': ('f', 3),
                    },
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            black=HalfMove(color=constants.BLACK, change={
                'WHITE': {},
                'BLACK': {
                    'N1': {
                        'old_position': ('b', 8),
                        'new_position': ('c', 6),
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change={
                    'WHITE': {
                        'B2': {
                            'old_position': ('f', 1),
                            'new_position': ('b', 5),
                        },
                    },
                    'BLACK': {},
                    'disambiguation': '',
                    'check': False,
                    'game_result': '',
                }),
                black=HalfMove(color=constants.BLACK, change={
                    'WHITE': {},
                    'BLACK': {
                        'AP': {
                            'old_position': ('a', 7),
                            'new_position': ('a', 6),
                        }
                    },
                    'disambiguation': '',
                    'check': False,
                    'game_result': '',
                }),
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
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'EP': {
                        'old_position': ('e', 2),
                        'new_position': ('e', 4),
                    },
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            black=HalfMove(color=constants.BLACK, change={
                'WHITE': {},
                'BLACK': {
                    'EP': {
                        'old_position': ('e', 7),
                        'new_position': ('e', 5),
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change={
                    'WHITE': {
                        'N2': {
                            'old_position': ('g', 1),
                            'new_position': ('f', 3),
                        },
                    },
                    'BLACK': {},
                    'disambiguation': '',
                    'check': False,
                    'game_result': '',
                }),
                black=HalfMove(color=constants.BLACK, change={
                    'WHITE': {},
                    'BLACK': {
                        'N1': {
                            'old_position': ('b', 8),
                            'new_position': ('c', 6),
                        }
                    },
                    'disambiguation': '',
                    'check': False,
                    'game_result': '',
                }),
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
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'EP': {
                        'old_position': ('e', 2),
                        'new_position': ('e', 4),
                    },
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            black=HalfMove(color=constants.BLACK, change={
                'WHITE': {},
                'BLACK': {
                    'EP': {
                        'old_position': ('e', 7),
                        'new_position': ('e', 5),
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            child=FullMove(
                white=HalfMove(color=constants.WHITE, change={
                    'WHITE': {
                        'N2': {
                            'old_position': ('g', 1),
                            'new_position': ('f', 3),
                        },
                    },
                    'BLACK': {},
                    'disambiguation': '',
                    'check': False,
                    'game_result': '',
                }),
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
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'EP': {
                        'old_position': ('e', 2),
                        'new_position': ('e', 4),
                    },
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            black=HalfMove(color=constants.BLACK, change={
                'WHITE': {},
                'BLACK': {
                    'EP': {
                        'old_position': ('e', 7),
                        'new_position': ('e', 5),
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
            child=FullMove(),
        )


@pytest.fixture
def half_move_tree():
    """
    1. e4
    """

    return FullMove(
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'EP': {
                        'old_position': ('e', 2),
                        'new_position': ('e', 4),
                    },
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
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
        white=HalfMove(color=constants.WHITE, change={
            'WHITE': {
                'EP': {
                    'old_position': ('e', 2),
                    'new_position': ('e', 4),
                },
            },
            'BLACK': {},
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }),
        black=HalfMove(color=constants.BLACK, change={
            'WHITE': {},
            'BLACK': {
                'DP': {
                    'old_position': ('d', 7),
                    'new_position': ('d', 5),
                }
            },
            'disambiguation': '',
            'check': False,
            'game_result': '',
        }),
        child=FullMove(
            white=HalfMove(color=constants.WHITE, change={
                'WHITE': {
                    'EP': {
                        'old_position': ('e', 4),
                        'new_position': ('d', 5),
                    },
                },
                'BLACK': {
                    'DP': {
                        'old_position': ('d', 5),
                        'new_position': None,
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            }),
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
                'WHITE': {
                    'K': {
                        'old_position': ('e', 1),
                        'new_position': ('g', 1),
                        'has_moved': True,
                    },
                    'R2': {
                        'old_position': ('h', 1),
                        'new_position': ('f', 1),
                        'has_moved': True,
                    }
                },
                'BLACK': {},
                'disambiguation': '',
                'check': False,
                'game_result': '',
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
                'WHITE': {
                    'Q2': {
                        'old_position': ('h', 4),
                        'new_position': ('e', 1),
                    }
                },
                'BLACK': {
                    'Q1': {
                        'old_position': ('e', 1),
                        'new_position': None,
                    }
                },

                # There are other white queens on both the h-file and 4-rank
                'disambiguation': 'h4',
                # Other possible keywords:
                'check': True,
                'game_result': '1-0',
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def white_pawn_promotion_to_queen():
    # fxg8=Q

    # What we really need is to construct these scenarios using
    # manual_move() and random_move(), output the tree, then
    # autoformat (using black?)

    return FullMove(
        white=HalfMove(
            color=constants.WHITE,
            change={
                'WHITE': {
                    'GP': {
                        'old_position': ('f', 7),
                        'new_position': None,
                    },
                    'Q2': {
                        'old_position': None,
                        'new_position': ('g', 8),
                        'piece_type': Queen,
                    }
                },
                'BLACK': {
                    'R2': {
                        'old_position': ('g', 8),
                        'new_position': None,
                    }
                },
                'disambiguation': '',
                'check': False,
                'game_result': '',
            },
        ),
        black=None,
        child=None,
    )


@pytest.fixture
def empty_change():
    return {
        'WHITE': {},
        'BLACK': {},
        'disambiguation': '',
        'check': False,
        'game_result': '',
    }
