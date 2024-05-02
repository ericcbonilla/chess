from dataclasses import dataclass, field

from .processor import Processor


# TODO Maybe FENProcessor could be memoized?
@dataclass(kw_only=True)
class FENProcessor(Processor):
    fen: str
    halfmove_clock: int = field(init=False)
    fullmove_number: int = field(init=False)

    def _convert(self):
        # ...do some operations on self.fen

        self.white = []
        self.black = []
