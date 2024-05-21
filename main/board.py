import os
from copy import deepcopy
from typing import TYPE_CHECKING, Optional

from colorist import yellow

from main import constants
from main.game_tree import FullMove, HalfMove
from main.types import Change, GameResult
from main.xposition import XPosition

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
        max_moves: int,
        game_tree: Optional[FullMove] = None,
        halfmove_clock: Optional[int] = 0,
        fullmove_number: Optional[int] = 1,
    ):
        self.max_moves = max_moves
        self.game_tree = game_tree or FullMove()
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number
        self.result: GameResult = None

        self._white = None
        self._black = None

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

    def to_fen(self):
        pass

    def to_pgn(self):
        pass

    @staticmethod
    def add_piece(piece: "Piece", attr: str):
        setattr(piece.agent, attr, piece)

        if hasattr(piece.agent.graveyard, attr):
            setattr(piece.agent.graveyard, attr, None)

    @staticmethod
    def destroy_piece(piece: "Piece", attr: str):
        setattr(piece.agent.graveyard, attr, piece)
        setattr(piece.agent, attr, None)

    def apply_change(self, change: Change):
        """
        All game state changes (i.e. changes to Teams and Pieces) should happen
        here. State should never be changed from anywhere else.
        """

        for agent in (self.white, self.black):
            if change[agent.color]:
                for key, datum in change[agent.color].items():
                    existing_piece = getattr(agent, key)

                    if key == "en_passant_target":
                        agent.en_passant_target = datum[1]
                    elif datum["new_position"] is None:
                        self.destroy_piece(existing_piece, attr=key)
                    elif datum["old_position"] is None:
                        # We're either resurrecting a piece, or adding a promotee
                        x, y = datum["new_position"]
                        piece = datum["piece_type"](
                            attr=key,
                            agent=agent,
                            x=x,
                            y=y,
                        )
                        self.add_piece(piece, attr=key)
                    else:
                        x, y = datum["new_position"]
                        existing_piece.x, existing_piece.y = XPosition(x), y

                    if "has_moved" in datum:
                        existing_piece.has_moved = datum["has_moved"]

        if "game_result" in change and change["game_result"]:
            self.result = change["game_result"]

    def apply_gametree(self, tree: FullMove):
        def _apply_next(node: FullMove):
            if node.is_empty():
                return
            elif node.child is None:
                self.apply_halfmove(node.white)
                return

            self.apply_halfmove(node.white)
            self.apply_halfmove(node.black)

            _apply_next(node.child)

        _apply_next(tree)

    def apply_halfmove(self, halfmove: HalfMove):
        # TODO We should convert to AN/PGN at this level or check Halfmove.to_an

        self.apply_change(halfmove.change)
        self.game_tree.append(halfmove)

    def rollback_halfmove(self, halfmove: Optional[HalfMove] = None):
        halfmove = halfmove or self.game_tree.get_latest_halfmove()
        inverted_change = deepcopy(constants.BLANK_CHANGE)

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

        self.apply_change(inverted_change)
        self.game_tree.prune()

    def play(self):
        term_size = os.get_terminal_size()

        while not self.result:
            if (self.fullmove_number - 1) == self.max_moves:
                break

            num_breaks = term_size.columns - len(str(self.fullmove_number)) - 2
            print(f"\n{self.fullmove_number}. {'=' * num_breaks}")

            # TODO determine who goes first based on halfmove_clock or whatever
            print(f"Turn: {constants.WHITE}")
            self.white.move()

            yellow(f"Turn: {constants.BLACK}")
            self.black.move()
            self.fullmove_number += 1

        return f"Moves played: {self.fullmove_number - 1}. Result: {self.result}"
