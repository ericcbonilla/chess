from dataclasses import dataclass, field

from main.game_tree import FullMove

from .processor import Processor


@dataclass(kw_only=True)
class PGNProcessor(Processor):
    pgn: str
    game_tree: FullMove = field(init=False)

    def _convert(self):
        # ...do some operations on self.pgn
        # TODO will need to backfill GameTree

        self.white = []
        self.black = []
