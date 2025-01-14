from functools import lru_cache
from operator import neg, pos
from typing import Callable, Optional

to_number_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
to_letter_map = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}


@lru_cache(maxsize=256)
def operate(operation: Callable, other: int, xpstr: str, wrap: bool) -> "XPosition":
    new_value = to_number_map[xpstr] + operation(other)

    if new_value not in to_letter_map:
        if wrap:
            new_value = ((new_value - operation(8)) % 8) or 8
        else:
            return XPosition("", wrap=wrap)

    return XPosition(to_letter_map[new_value], wrap=wrap)


class XPosition(str):
    __slots__ = ("wrap",)

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, _, wrap: Optional[bool] = False):
        self.wrap = wrap

    def __sub__(self, other: int):
        return operate(neg, other, str(self), self.wrap)

    def __add__(self, other: int):
        return operate(pos, other, str(self), self.wrap)

    def to_int(self) -> int:
        return to_number_map[self]
