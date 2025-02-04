from dataclasses import dataclass
from typing import Optional

from .halfmove import HalfMove


@dataclass(slots=True)
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

    def get_node_at_height(self, height: int) -> "FullMove":
        """
        height of 0 yields a leaf, height of 1 yields second to last node, etc.
        """

        return [*self][-1 - height]
