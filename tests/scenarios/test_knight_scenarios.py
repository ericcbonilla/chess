import pytest

from main.exceptions import InvalidMoveError
from main.x import G


class TestKnightScenarios:
    def test_knight_cannot_move_in_straight_line(self, default_board):
        with pytest.raises(InvalidMoveError):
            default_board.white.move("g_knight", G, 3)
