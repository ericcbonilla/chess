from tabulate import tabulate

from .fullmove import FullMove
from .halfmove import HalfMove


# TODO try to unify all tree traversal code
def pprint(root: FullMove):
    data = []

    def _add_row(idx: int, node: FullMove):
        if node.is_empty():
            return

        row = [idx]
        if node.white:
            row.append(node.white.change)
        if node.black:
            row.append(node.black.change)
        data.append(row)

        if node.child:
            return _add_row(idx + 1, node.child)

    _add_row(1, root)

    table = tabulate(
        data,
        headers=["", "White", "Black"],
        tablefmt="grid",
        maxcolwidths=[None, 60, 60],
    )
    print(table)


def traverse():
    pass


def get_halfmove(idx: float, node: FullMove | None) -> HalfMove:
    if node is None or node.is_empty():
        raise Exception(f"Halfmove {idx} not found")
    elif halfmove := node.black if str(idx).endswith(".5") else node.white:
        if halfmove.change["fullmove_number"][0] == int(idx):
            return halfmove

    return get_halfmove(idx, node.child)
