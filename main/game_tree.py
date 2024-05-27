from dataclasses import dataclass
from typing import Optional

from tabulate import tabulate

from main import constants
from main.types import AgentColor, Change


@dataclass
class FullMove:
    white: Optional["HalfMove"] = None
    black: Optional["HalfMove"] = None
    child: Optional["FullMove"] = None

    def is_empty(self) -> bool:
        return self.white is None and self.black is None and self.child is None

    def pprint(self):
        data = []

        def _add_row(idx: int, node: FullMove):
            if node.is_empty():
                return

            row = [idx]
            if node.white:
                row.append(node.white.change)
            if node.black:
                row.append(node.black.change)
            data.append(row)

            if node.child:
                return _add_row(idx + 1, node.child)

        _add_row(1, self)

        table = tabulate(
            data,
            headers=["", "White", "Black"],
            tablefmt="grid",
            maxcolwidths=[None, 60, 60],
        )
        print(table)

    def _get_node_at_height(self, height: int) -> "FullMove":
        """
        height of 0 yields a leaf, height of 1 yields second to last node, etc.
        """

        nodes = [self]

        def _get_next(node: FullMove):
            if not node.child:
                return
            nodes.append(node.child)
            _get_next(node.child)

        _get_next(self)
        return nodes[-1 - height]

    def append(self, halfmove: "HalfMove"):
        node = self._get_node_at_height(0)
        if halfmove.color == constants.WHITE:
            node.white = halfmove
        else:
            node.black = halfmove
            # The next FullMove is added once the current node is full
            node.child = FullMove()

    def get_latest_halfmove(self) -> "HalfMove":
        if self.child is None:
            return self.white
        elif self.child.is_empty():  # Removing second move
            return self.black

        fullmove = self._get_node_at_height(1)
        if fullmove.child.is_empty():
            return fullmove.black
        else:
            return fullmove.child.white

    def prune(self):
        # TODO eventually we might need to prune a branch larger than just one halfmove
        # (pruning a non-leaf node and its children)
        # We'll also have to revert to allowing more than one child

        if self.child is None:
            self.white = None  # Remove first move; we've fully reset the board
            return
        elif self.child.is_empty():  # Removing second move
            self.black = None
            self.child = None
            return

        fullmove = self._get_node_at_height(1)
        if fullmove.child.is_empty():
            # Pruning a black node
            fullmove.black = None
            fullmove.child = None
        else:
            # Pruning a white node
            fullmove.child = FullMove()


@dataclass
class HalfMove:
    """
    Contains all the necessary information to:
    - Generate algebraic notation for this move
    - Show the exact state changes that occurred due to this move
    - Reverse those changes if we want to rollback this move

    The general shape of the change dict is shown in the example below.

    {
        # We will always have two items, represented as dicts, for each Agent. If
        # no change needs to be made for an Agent, the dict will be empty.
        constants.WHITE: {
            # Denotes a rook moving
            'R1': {
                'old_position': ('a', 1),
                'new_position': ('a', 3),

                # Only for Kings and Rooks. Used to compute castle legality
                'has_moved': True,
            }
        },
        constants.BLACK: {
            # Denotes an en passant target expiring
            'en_passant_target': (('d', 6), None),

            # Denotes a pawn being captured
            'DP': {
                'old_position': ('d', 5),
                'new_position': None,
            }
        },

        # These last three items are only ever used to generate algebraic notation;
        # there are no state changes made based on these values
        'disambiguation': '',
        'check': False,
        'game_result': None,
    }
    """

    color: AgentColor
    change: Change

    def to_an(self) -> str:
        pass
