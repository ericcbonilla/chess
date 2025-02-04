import os
from collections import Counter
from datetime import date
from typing import TYPE_CHECKING, Dict, Optional

import pyperclip
from colorist import Color

from main import constants
from main.exceptions import NotFoundError
from main.game_tree import FullMove, GameTree, HalfMove
from main.game_tree.utils import get_halfmove
from main.notation.utils import truncate_fen
from main.types import Change, GameResult, Position
from main.utils import cprint, print_move_heading
from main.x import H, to_str

if TYPE_CHECKING:
    from main.agents import Agent
    from main.pieces import Piece


class Board:
    """
     The highest-level object in our data model. All game information
     can be accessed here: Agents, Pieces, prior moves. The board knows all.

    Responsibilities:
    - Apply game state Changes (Moving pieces)
        - Needs to be at the Board level because changes can affect both Agents
    - Maintain GameTree
    - Manage gameplay (Tell an Agent it's his turn to move)
    - Assign Pieces to Agents upon creation
    - Offer access to both Agents
    """

    def __init__(
        self,
        max_fullmoves: int,
        active_color: Optional[str] = None,
        halfmove_clock: Optional[int] = 0,
        fullmove_number: Optional[int] = 1,
        game_tree: Optional[GameTree] = None,
        fen_cts: Optional[Dict] = None,
    ):
        self.max_fullmoves = max_fullmoves
        self.game_tree = game_tree or GameTree()
        self.active_color = active_color or "w"
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number
        self.fen_cts = fen_cts
        self.result: GameResult = None

        self._white = None
        self._black = None

    __slots__ = (
        "max_fullmoves",
        "game_tree",
        "active_color",
        "halfmove_clock",
        "fullmove_number",
        "fen_cts",
        "result",
        "_white",
        "_black",
    )

    def __repr__(self) -> str:
        return f"{self.white}{self.white.graveyard}\n\n{self.black}{self.black.graveyard}\n"

    @property
    def white(self) -> "Agent":
        return self._white

    @property
    def black(self) -> "Agent":
        return self._black

    @white.setter
    def white(self, agent: "Agent"):
        self._white = agent

    @black.setter
    def black(self, agent: "Agent"):
        self._black = agent

    @property
    def truncated_result(self) -> str:
        return self.result[0:3] if self.result else ""

    @property
    def active_agent(self) -> "Agent":
        return self.white if self.active_color == "w" else self.black

    @staticmethod
    def _get_row(
        y: int, white_memo: Dict[Position, str], black_memo: Dict[Position, str]
    ) -> str:
        row = ""
        empty_squares_ct = 0

        for x in constants.FILES:
            if piece := white_memo.get((x, y)) or black_memo.get((x, y)):
                row += f"{str(empty_squares_ct) if empty_squares_ct else ''}{piece}"
                empty_squares_ct = 0
            elif x == H:
                row += str(empty_squares_ct + 1)
            else:
                empty_squares_ct += 1

        return row if y == 1 else f"{row}/"

    def get_fen(
        self, idx: Optional[float] = None, internal: Optional[bool] = False
    ) -> str:
        # TODO Look into optimizing this

        if idx:
            halfmove = get_halfmove(idx, self.game_tree.root)
            return halfmove.change["fen"]

        piece_placement = ""
        white_memo = {p.position: p.fen_symbol for p in self.white.pieces.values()}
        black_memo = {
            p.position: p.fen_symbol.lower() for p in self.black.pieces.values()
        }
        for y in constants.RANKS:
            piece_placement += self._get_row(y, white_memo, black_memo)

        castling_rights = (
            self.white.castling_rights + self.black.castling_rights.lower()
        ) or "-"

        if target := self.white.en_passant_target or self.black.en_passant_target:
            x, y = target
            en_passant_target = f"{to_str(x)}{str(y)}"
        else:
            en_passant_target = "-"

        fen = (
            f"{piece_placement} {self.active_color} {castling_rights} "
            f"{en_passant_target} {self.halfmove_clock} {self.fullmove_number}"
        )

        if internal:
            return fen
        else:
            print(fen)
            pyperclip.copy(fen)
            print("\nCopied to clipboard!")
            return fen

    def _get_movetext(
        self, compact: Optional[bool] = True, colored: Optional[bool] = True
    ) -> str:
        movetext = ""
        for node in self.game_tree.root:
            if node.is_empty():
                break
            number, _ = (node.white or node.black).change["fullmove_number"]
            white_an = node.white.to_an() if node.white else "..."
            black_an = node.black.to_an() if node.black else ""
            if colored:
                white_color = Color.RED if "x" in white_an else Color.WHITE
                black_color = Color.RED if "x" in black_an else Color.YELLOW
                off = Color.OFF
            else:
                white_color, black_color, off = "", "", ""
            movetext += (
                f"{number}. {white_color}{white_an}{off} "
                f"{black_color}{black_an}{off}{" " if compact else "\n"}"
            )
        return movetext + self.truncated_result

    def get_pgn(self, compact: Optional[bool] = True):
        pgn = (
            f'[Event "?"]\n'
            f'[Site "?"]\n'
            f"[Date \"{date.today().strftime('%Y.%m.%d')}\"]\n"
            f'[Round "?"]\n'
            f'[Result "{self.truncated_result}"]\n'
            f'[White "{self.white.__class__.__name__}"]\n'
            f'[Black "{self.black.__class__.__name__}"]\n\n'
        )

        print(f"{pgn}{self._get_movetext(compact=compact)}")
        pyperclip.copy(f"{pgn}{self._get_movetext(compact=compact, colored=False)}")
        print("\nCopied to clipboard!")

    @staticmethod
    def add_piece(piece: "Piece", attr: str, new_position: Position):
        piece.agent.pieces_cache[new_position] = piece
        setattr(piece.agent, attr, piece)

        if hasattr(piece.agent.graveyard, attr):
            setattr(piece.agent.graveyard, attr, None)

    @staticmethod
    def destroy_piece(piece: "Piece", attr: str):
        piece.agent.del_cache_item((piece.x, piece.y))

        setattr(piece.agent.graveyard, attr, piece)
        setattr(piece.agent, attr, None)

    def apply_change(self, change: Change, rollback: Optional[bool] = False):
        """
        All game state changes (i.e. changes to Board, Agents, and Pieces) should happen
        here. State should never be changed from anywhere else.
        """

        for agent in (self.white, self.black):
            if change[agent.color]:
                for key, datum in change[agent.color].items():
                    piece = getattr(agent, key)

                    if key == "en_passant_target":
                        agent.en_passant_target = datum[1]
                    elif datum["new_position"] is None:
                        self.destroy_piece(piece, attr=key)
                    elif datum["old_position"] is None:
                        # We're either resurrecting a piece, or adding a promotee
                        x, y = datum["new_position"]
                        piece = datum["piece_type"](
                            attr=key,
                            agent=agent,
                            x=x,
                            y=y,
                        )
                        self.add_piece(piece, attr=key, new_position=(x, y))
                    else:
                        agent.del_cache_item((piece.x, piece.y))
                        x, y = datum["new_position"]
                        piece.x, piece.y = x, y
                        agent.pieces_cache[(x, y)] = piece

                    if "has_moved" in datum:
                        piece.has_moved = datum["has_moved"]

        if "game_result" in change and change["game_result"]:
            self.result = change["game_result"]
        if "fen" in change:
            if rollback:
                self.fen_cts[truncate_fen(change["fen"])] -= 1
            else:
                self.fen_cts[truncate_fen(change["fen"])] += 1

        self.halfmove_clock = change["halfmove_clock"][1]
        self.active_color = "w" if self.active_color == "b" else "b"
        self.fullmove_number = change["fullmove_number"][1]

    def apply_gametree(self, root: FullMove):
        for node in root:
            if node.white:
                self.apply_halfmove(node.white)
            if node.black:
                self.apply_halfmove(node.black)

    def apply_halfmove(self, halfmove: HalfMove):
        self.apply_change(halfmove.change)
        self.game_tree.append(halfmove)

    def rollback_halfmove(self, halfmove: Optional[HalfMove] = None):
        halfmove = halfmove or self.game_tree.get_latest_halfmove()
        inverted_change = {
            constants.WHITE: {},
            constants.BLACK: {},
            "disambiguation": "",
            "check": False,
            "game_result": None,
            "symbol": None,
        }

        for agent in (self.white, self.black):
            if halfmove.change[agent.color]:
                for key, datum in halfmove.change[agent.color].items():
                    if key == "en_passant_target":
                        inverted_change[agent.color][key] = (datum[1], datum[0])
                        continue

                    inverted_change[agent.color][key] = {
                        "old_position": datum["new_position"],
                        "new_position": datum["old_position"],
                    }

                    if getattr(agent.graveyard, key):
                        inverted_change[agent.color][key]["piece_type"] = type(
                            getattr(agent.graveyard, key)
                        )
                    if "has_moved" in datum:
                        inverted_change[agent.color][key]["has_moved"] = not datum[
                            "has_moved"
                        ]

        if (
            "game_result" in halfmove.change
            and halfmove.change["game_result"] is not None
        ):
            inverted_change["result"] = None

        inverted_change["halfmove_clock"] = (
            halfmove.change["halfmove_clock"][1],
            halfmove.change["halfmove_clock"][0],
        )
        inverted_change["fullmove_number"] = (
            halfmove.change["fullmove_number"][1],
            halfmove.change["fullmove_number"][0],
        )

        self.apply_change(inverted_change, rollback=True)
        self.game_tree.prune()

    def has_insufficient_material(self) -> bool:
        scenarios = [
            ([0], [0]),  # KK
            ([0], [0, 3]),  # KKN or KKB
            ([0, 3], [0]),  # KNK or KBK
        ]

        if self.white.material_sum > 3 or self.black.material_sum > 3:
            return False
        for white_material, black_material in scenarios:
            white_match = Counter(self.white.material) == Counter(white_material)
            black_match = Counter(self.black.material) == Counter(black_material)
            if white_match and black_match:
                return True

        if Counter(self.white.material) == Counter([0, 3]) and Counter(
            self.black.material
        ) == Counter([0, 3]):
            try:
                white_bishop = self.white.get_bishop()
                black_bishop = self.black.get_bishop()
            except NotFoundError:
                return False

            return white_bishop.dark is black_bishop.dark

        return False

    def draw_by_repetition(self, fen: str) -> bool:
        return self.fen_cts[truncate_fen(fen)] == 2

    def play(self, num_fullmoves: Optional[int] = None):
        term_size = os.get_terminal_size()
        elapsed_fullmoves = 0

        if not self.result and self.active_agent is self.black:
            print_move_heading(term_size, self.fullmove_number)
            cprint(f"Turn: {constants.WHITE}\n...")
            self.black.move()
            elapsed_fullmoves += 1

        while not self.result:
            if (self.fullmove_number - 1) == self.max_fullmoves:
                break
            if num_fullmoves is not None and elapsed_fullmoves == num_fullmoves:
                break

            print_move_heading(term_size, self.fullmove_number)
            self.white.move()

            if not self.result:
                self.black.move()
                elapsed_fullmoves += 1

        print(f"\nMoves played: {self.fullmove_number - 1}. Result: {self.result}")
