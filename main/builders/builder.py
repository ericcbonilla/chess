from typing import TYPE_CHECKING, List, Optional, Type

from main import constants
from main.board import Board
from main.exceptions import SlotError
from main.pieces import Bishop, King, Knight, Queen, Rook
from main.types import AgentScaffold, PieceScaffold
from main.xposition import XPosition

from .scaffolds import BLACK_SCAFFOLD, EMPTY_SCAFFOLD, WHITE_SCAFFOLD

if TYPE_CHECKING:
    from main.agents import Agent


# TODO Do we want one unified builder or multiple (for FEN, PGN, default, ...)
class BoardBuilder:
    @staticmethod
    def _get_board(
        white_agent_cls: Type["Agent"], black_agent_cls: Type["Agent"], max_moves: int
    ):
        board = Board(max_moves=max_moves)
        # TODO https://youtrack.jetbrains.com/issue/PY-36375/Unexpected-argument-false-positive-when-reassigning-a-dataclass-PEP-557
        # noinspection PyArgumentList
        board.white = white_agent_cls(color=constants.WHITE, board=board)
        # noinspection PyArgumentList
        board.black = black_agent_cls(color=constants.BLACK, board=board)

        return board

    @staticmethod
    def _set_pieces(agent: "Agent", opponent_agent: "Agent", scaffold: AgentScaffold):
        for attr, data in scaffold.items():
            if data is None:
                continue

            piece = data["piece_type"](
                attr=attr,
                agent=agent,
                opponent_agent=opponent_agent,
                x=data["x"],
                y=data["y"],
                **({"has_moved": data["has_moved"]} if "has_moved" in data else {}),
            )

            setattr(agent, attr, piece)

    def from_start(
        self,
        white_agent_cls: Type["Agent"],
        black_agent_cls: Type["Agent"],
        max_moves: Optional[int] = 50,
    ):
        board = self._get_board(white_agent_cls, black_agent_cls, max_moves)

        self._set_pieces(
            agent=board.white,
            opponent_agent=board.black,
            scaffold=WHITE_SCAFFOLD,
        )

        self._set_pieces(
            agent=board.black,
            opponent_agent=board.white,
            scaffold=BLACK_SCAFFOLD,
        )

        return board

    def _get_slot(
        self, scaffold: AgentScaffold, datum: PieceScaffold, x1: str, x2: str, name: str
    ) -> str:
        if scaffold[f"{x1}_{name}"] and scaffold[f"{x2}_{name}"]:
            return self._get_promotion_slot(scaffold, datum)
        elif datum["x"] in (x1, x2) and scaffold[f"{datum['x']}_{name}"] is None:
            return f"{datum['x']}_{name}"
        elif scaffold[f"{x1}_{name}"] is None:
            return f"{x1}_{name}"
        else:
            return f"{x2}_{name}"

    @staticmethod
    def _get_file_slot(scaffold: AgentScaffold, datum: PieceScaffold, name: str) -> str:
        x = XPosition(datum["x"], wrap=True)
        slot = None

        while not slot:
            if scaffold[f"{x}_{name}"] is None:
                slot = f"{x}_{name}"
            else:
                x += 1
                if x == datum["x"]:
                    raise SlotError(
                        f"Could not add {datum['piece_type']} at "
                        f"{(datum['x'], datum['y'])}; all slots taken"
                    )

        return slot

    def _get_promotion_slot(self, scaffold: AgentScaffold, datum: PieceScaffold) -> str:
        return self._get_file_slot(scaffold, datum, "prom")

    def _get_pawn_slot(self, scaffold: AgentScaffold, datum: PieceScaffold) -> str:
        return self._get_file_slot(scaffold, datum, "pawn")

    def _get_scaffold(self, piece_data: List[PieceScaffold]):
        scaffold = EMPTY_SCAFFOLD.copy()

        for datum in piece_data:
            if datum["piece_type"] is King:
                slot = "king"
            elif datum["piece_type"] is Queen:
                if scaffold["queen"] is None:
                    slot = "queen"
                else:
                    slot = self._get_promotion_slot(scaffold, datum)
            elif datum["piece_type"] is Rook:
                slot = self._get_slot(scaffold, datum, "a", "h", "rook")
            elif datum["piece_type"] is Knight:
                slot = self._get_slot(scaffold, datum, "b", "g", "knight")
            elif datum["piece_type"] is Bishop:
                slot = self._get_slot(scaffold, datum, "c", "f", "bishop")
            else:
                slot = self._get_pawn_slot(scaffold, datum)

            scaffold[slot] = datum

        return scaffold

    # TODO add tests for this:
    # - 8 Promotees
    # - Multiple pawns on file
    def from_data(
        self,
        white_agent_cls: Type["Agent"],
        black_agent_cls: Type["Agent"],
        white_data: List[PieceScaffold],
        black_data: List[PieceScaffold],
        max_moves: Optional[int] = 50,
    ):
        board = self._get_board(white_agent_cls, black_agent_cls, max_moves)

        self._set_pieces(
            agent=board.white,
            opponent_agent=board.black,
            scaffold=self._get_scaffold(white_data),
        )

        self._set_pieces(
            agent=board.black,
            opponent_agent=board.white,
            scaffold=self._get_scaffold(black_data),
        )

        return board

    # @classmethod
    # def from_fen(
    #     cls,
    #     white_agent_cls: Type['Agent'],
    #     black_agent_cls: Type['Agent'],
    #     fen: str,
    #     max_moves: Optional[int] = 50,
    # ):
    #     processor = FENProcessor(fen=fen)
    #
    #     return cls(
    #         max_moves=max_moves,
    #         white=white_agent_cls.from_collection(
    #             color=constants.WHITE, coll=processor.white
    #         ),
    #         black=black_agent_cls.from_collection(
    #             color=constants.BLACK, coll=processor.black
    #         ),
    #         halfmove_clock=processor.halfmove_clock,
    #         fullmove_number=processor.fullmove_number,
    #     )
    #
    # @classmethod
    # def from_pgn(
    #     cls,
    #     white_agent_cls: Type['Agent'],
    #     black_agent_cls: Type['Agent'],
    #     pgn: str,
    #     max_moves: Optional[int] = 50,
    # ):
    #     processor = PGNProcessor(pgn=pgn)
    #
    #     return cls(
    #         max_moves=max_moves,
    #         white=white_agent_cls.from_collection(
    #             color=constants.WHITE, coll=processor.white
    #         ),
    #         black=black_agent_cls.from_collection(
    #             color=constants.BLACK, coll=processor.black
    #         ),
    #         game_tree=processor.game_tree,
    #     )
