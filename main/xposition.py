from operator import neg, pos
from typing import Callable, Optional


class XPosition(str):
    to_number_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    to_letter_map = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, _, wrap: Optional[bool] = False):
        self.wrap = wrap

    def _operate(self, operation: Callable, other: int) -> "XPosition":
        new_value = self.to_number_map[self] + operation(other)

        if new_value not in self.to_letter_map:
            if self.wrap:
                new_value = ((new_value - operation(8)) % 8) or 8
            else:
                return XPosition("", wrap=self.wrap)

        return XPosition(self.to_letter_map[new_value], wrap=self.wrap)

    def __sub__(self, other: int):
        return self._operate(neg, other)

    def __add__(self, other: int):
        return self._operate(pos, other)
