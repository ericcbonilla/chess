from typing import Optional

from main import constants

from .fullmove import FullMove
from .halfmove import HalfMove


class GameTree:
    def __init__(self):
        self.root: FullMove = FullMove()
        self.latest_fullmove: FullMove = self.root
        self.second_latest_fullmove: Optional[FullMove] = None
        self.third_latest_fullmove: Optional[FullMove] = None

    @classmethod
    def backfill(cls, root: FullMove) -> "GameTree":
        tree = cls()
        for node in root:
            if node.white:
                tree.append(node.white)
            if node.black:
                tree.append(node.black)

        return tree

    def append(self, hm: "HalfMove"):
        node = self.latest_fullmove

        if hm.color == constants.WHITE:
            node.white = hm
        else:
            node.black = hm
            # The next FullMove is added once the current node is full
            self.latest_fullmove = node.child = FullMove()
            self.third_latest_fullmove = self.second_latest_fullmove
            self.second_latest_fullmove = node

    def prune(self):
        # TODO eventually we might need to prune a branch larger than just one halfmove
        # (pruning a non-leaf node and its children)
        # We'll also have to revert to allowing more than one child

        if self.root.child is None:
            self.root.white = None  # Remove first move; we've fully reset the board
            return
        elif self.root.child.is_empty():  # Removing second move
            self.root.black = None
            self.root.child = None
            self.latest_fullmove = self.root
            self.second_latest_fullmove = None
            return

        fm = self.second_latest_fullmove
        if fm.child.is_empty():
            # Pruning a black node
            fm.black = None
            fm.child = None
            self.latest_fullmove = self.second_latest_fullmove
            self.second_latest_fullmove = self.third_latest_fullmove
            self.third_latest_fullmove = None
        else:
            # Pruning a white node
            fm.child = FullMove()
            self.latest_fullmove = fm.child

    def get_latest_halfmove(self) -> Optional["HalfMove"]:
        if self.second_latest_fullmove is None:
            if self.root.black:
                return self.root.black
            elif self.root.white:
                return self.root.white
        else:
            fm = self.second_latest_fullmove
            if fm.child.is_empty():
                return fm.black
            else:
                return fm.child.white
