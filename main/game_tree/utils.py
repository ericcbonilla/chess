from typing import TYPE_CHECKING

from tabulate import tabulate

from main.utils import cprint

if TYPE_CHECKING:
    from .fullmove import FullMove
    from .halfmove import HalfMove


def pprint(root: "FullMove"):
    data = []

    for node in root:
        if node.is_empty():
            return

        row = [(node.white or node.black).change["fullmove_number"][0]]
        if node.white:
            row.append(node.white.change)
        if node.black:
            row.append(node.black.change)
        data.append(row)

    table = tabulate(
        data,
        headers=["", "White", "Black"],
        tablefmt="grid",
        maxcolwidths=[None, 60, 60],
    )
    cprint(table)


def get_halfmove(idx: float, root: "FullMove") -> "HalfMove":
    for node in root:
        if halfmove := node.black if str(idx).endswith(".5") else node.white:
            if halfmove.change["fullmove_number"][0] == int(idx):
                return halfmove
    else:
        raise Exception(f"Halfmove {idx} not found")
