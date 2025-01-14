import os
from typing import Callable, Optional, Tuple

from colorist import white, yellow
from dotenv import load_dotenv

from main import constants
from main.types import AgentColor, Position

load_dotenv()


def cprint(
    message: str,
    agent_color: Optional[AgentColor] = None,
    color_fn: Optional[Callable] = None,
):
    if not int(os.getenv("DEBUG")):
        return
    elif agent_color is None:
        print(message)
        return

    color_fn = color_fn or (yellow if agent_color == constants.BLACK else white)
    color_fn(message)


def print_move_heading(term_size, fullmove_number: int):
    num_breaks = term_size.columns - len(str(fullmove_number)) - 2
    cprint(f"\n{fullmove_number}. {'=' * num_breaks}")


def vector(position: Position, other: Position) -> Tuple[int, int]:
    x, y = position
    other_x, other_y = other

    return abs(x.to_int() - other_x.to_int()), abs(y - other_y)
