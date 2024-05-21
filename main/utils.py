from typing import Callable, Optional

from colorist import white, yellow

from main import constants
from main.types import AgentColor


def cprint(agent_color: AgentColor, message: str, color_fn: Optional[Callable] = None):
    color_fn = color_fn or (yellow if agent_color == constants.BLACK else white)
    color_fn(message)
