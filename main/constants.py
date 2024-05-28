from typing import List

from main.types import AgentColor

WHITE = "WHITE"
BLACK = "BLACK"
COLORS: List[AgentColor] = ["WHITE", "BLACK"]
BLANK_CHANGE = {
    WHITE: {},
    BLACK: {},
    "disambiguation": "",
    "check": False,
    "game_result": None,
    "symbol": None,
}


RANKS = [8, 7, 6, 5, 4, 3, 2, 1]
FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
SQUARES = {(f, r) for f in FILES for r in RANKS}


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
