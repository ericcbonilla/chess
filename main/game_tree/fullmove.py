from dataclasses import dataclass
from typing import Optional

from main import constants

from .halfmove import HalfMove


@dataclass
class FullMove:
    white: Optional["HalfMove"] = None
    black: Optional["HalfMove"] = None
    child: Optional["FullMove"] = None

    def __iter__(self):
        yield self
        if self.child:
            yield from self.child

    def is_empty(self) -> bool:
        return self.white is None and self.black is None and self.child is None

    def _get_node_at_height(self, height: int) -> "FullMove":
        """
        height of 0 yields a leaf, height of 1 yields second to last node, etc.
        """

        return [*self][-1 - height]

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
        elif self.child.is_empty():
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
