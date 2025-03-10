from typing import List

from main.types import AgentColor
from main.x import A, B, C, D, E, F, G, H

WHITE = "WHITE"
BLACK = "BLACK"
COLORS: List[AgentColor] = ["WHITE", "BLACK"]
RANKS = [8, 7, 6, 5, 4, 3, 2, 1]
FILES = [A, B, C, D, E, F, G, H]

SQUARES_LIST = [(f, r) for r in RANKS for f in FILES]
SQUARES = set(SQUARES_LIST)
DARK_SQUARES = {
    *[(f, r) for r in RANKS[::2] for f in FILES[1::2]],
    *[(f, r) for r in RANKS[1::2] for f in FILES[::2]],
}


PIECE_ATTRS = (
    "king",
    "queen",
    "a_rook",
    "h_rook",
    "b_knight",
    "g_knight",
    "c_bishop",
    "f_bishop",
    "a_pawn",
    "b_pawn",
    "c_pawn",
    "d_pawn",
    "e_pawn",
    "f_pawn",
    "g_pawn",
    "h_pawn",
    "a_prom",
    "b_prom",
    "c_prom",
    "d_prom",
    "e_prom",
    "f_prom",
    "g_prom",
    "h_prom",
)
