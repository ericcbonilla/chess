import itertools
import re
from collections import defaultdict
from typing import TYPE_CHECKING, List, Optional, Type

from main import constants
from main.agents import ManualAgent
from main.board import Board
from main.exceptions import BuildError
from main.notation import FEN
from main.notation.utils import truncate_fen
from main.pieces import SYMBOLS_MAP, Bishop, King, Knight, Queen, Rook
from main.types import AgentScaffold, PieceScaffold, X
from main.x import A, B, C, F, G, H, to_str

from .scaffolds import BLACK_SCAFFOLD, EMPTY_SCAFFOLD, WHITE_SCAFFOLD

if TYPE_CHECKING:
    from main.agents import Agent


# TODO Do we want one unified builder or multiple (for FEN, PGN, default, ...)
class BoardBuilder:
    @staticmethod
    def _get_board(
        white_agent_cls: Type["Agent"],
        black_agent_cls: Type["Agent"],
        max_fullmoves: int,
        active_color: str,
        halfmove_clock: Optional[int] = 0,
        fullmove_number: Optional[int] = 1,
    ) -> Board:
        board = Board(max_fullmoves, active_color, halfmove_clock, fullmove_number)
        # https://youtrack.jetbrains.com/issue/PY-36375/Unexpected-argument-false-positive-when-reassigning-a-dataclass-PEP-557
        # noinspection PyArgumentList
        board.white = white_agent_cls(color=constants.WHITE, board=board)
        # noinspection PyArgumentList
        board.black = black_agent_cls(color=constants.BLACK, board=board)

        return board

    @staticmethod
    def _set_pieces(agent: "Agent", scaffold: AgentScaffold):
        for attr, data in scaffold.items():
            if data is None:
                continue

            piece = data["piece_type"](
                attr=attr,
                agent=agent,
                x=data["x"],
                y=data["y"],
                **({"has_moved": data["has_moved"]} if "has_moved" in data else {}),
            )

            setattr(agent, attr, piece)

    def _get_slot(
        self,
        scaffold: AgentScaffold,
        datum: PieceScaffold,
        x1: X,
        x2: X,
        name: str,
    ) -> str:
        datum_str = to_str(datum["x"])

        if scaffold[f"{to_str(x1)}_{name}"] and scaffold[f"{to_str(x2)}_{name}"]:
            return self._get_promotion_slot(scaffold, datum)
        elif (
            datum_str in (to_str(x1), to_str(x2))
            and scaffold[f"{datum_str}_{name}"] is None
        ):
            return f"{datum_str}_{name}"
        elif scaffold[f"{to_str(x1)}_{name}"] is None:
            return f"{to_str(x1)}_{name}"
        else:
            return f"{to_str(x2)}_{name}"

    @staticmethod
    def _get_file_slot(scaffold: AgentScaffold, datum: PieceScaffold, name: str) -> str:
        x = datum["x"]
        slot = None

        while not slot:
            if scaffold[f"{to_str(x)}_{name}"] is None:
                slot = f"{to_str(x)}_{name}"
            else:
                x += 1
                if x not in [1, 8]:
                    x = ((x + 8) % 8) or 8
                if x == datum["x"]:
                    raise BuildError(
                        f"Could not add {datum['piece_type']} at "
                        f"{(datum['x'], datum['y'])}; all slots taken"
                    )

        return slot

    def _get_promotion_slot(self, scaffold: AgentScaffold, datum: PieceScaffold) -> str:
        return self._get_file_slot(scaffold, datum, "prom")

    def _get_pawn_slot(self, scaffold: AgentScaffold, datum: PieceScaffold) -> str:
        if datum["y"] in (1, 8):
            raise BuildError("Pawns cannot be on back ranks")
        return self._get_file_slot(scaffold, datum, "pawn")

    def _get_scaffold(self, piece_data: List[PieceScaffold]) -> AgentScaffold:
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
                slot = self._get_slot(scaffold, datum, A, H, "rook")
            elif datum["piece_type"] is Knight:
                slot = self._get_slot(scaffold, datum, B, G, "knight")
            elif datum["piece_type"] is Bishop:
                slot = self._get_slot(scaffold, datum, C, F, "bishop")
            else:
                slot = self._get_pawn_slot(scaffold, datum)

            scaffold[slot] = datum

        if scaffold["king"] is None:
            raise BuildError("Cannot build board with missing King")

        return scaffold

    def from_start(
        self,
        white_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        black_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        max_fullmoves: Optional[int] = 300,
    ) -> Board:
        board = self._get_board(white_agent_cls, black_agent_cls, max_fullmoves, "w")
        self._set_pieces(agent=board.white, scaffold=WHITE_SCAFFOLD)
        self._set_pieces(agent=board.black, scaffold=BLACK_SCAFFOLD)
        board.fen_cts = defaultdict(
            int, {"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": 1}
        )

        return board

    def from_data(
        self,
        white_data: List[PieceScaffold],
        black_data: List[PieceScaffold],
        white_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        black_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        max_fullmoves: Optional[int] = 300,
        active_color: Optional[str] = None,
    ) -> Board:
        board = self._get_board(
            white_agent_cls, black_agent_cls, max_fullmoves, active_color
        )
        self._set_pieces(agent=board.white, scaffold=self._get_scaffold(white_data))
        self._set_pieces(agent=board.black, scaffold=self._get_scaffold(black_data))
        board.fen_cts = defaultdict(
            int, {truncate_fen(board.get_fen(internal=True)): 1}
        )

        return board

    def from_fen(
        self,
        text: str,
        white_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        black_agent_cls: Optional[Type["Agent"]] = ManualAgent,
        max_fullmoves: Optional[int] = 300,
    ) -> Board:
        fen = FEN(text=text)
        iter_squares = iter(constants.SQUARES_LIST)
        white_data = []
        black_data = []

        for ch in fen.piece_placement:
            if ch == "/":
                continue
            elif re.match(r"\d", ch):
                next(itertools.islice(iter_squares, int(ch) - 1, None))
                continue

            x, y = next(iter_squares)
            scaffold = {"piece_type": SYMBOLS_MAP[ch], "x": x, "y": y}

            if scaffold["piece_type"] in (Rook, King) and (x, y) in fen.castling_rights:
                scaffold["has_moved"] = not fen.castling_rights[x, y]
            if ch.islower():
                black_data.append(scaffold)
            else:
                white_data.append(scaffold)

        board = self._get_board(
            white_agent_cls,
            black_agent_cls,
            max_fullmoves,
            active_color=fen.active_color,
            halfmove_clock=fen.halfmove_clock,
            fullmove_number=fen.fullmove_number,
        )
        board.fen_cts = defaultdict(int, {truncate_fen(text): 1})
        if fen.en_passant_target:
            inactive_agent = board.white if fen.active_color == "b" else board.black
            inactive_agent.en_passant_target = fen.en_passant_target

        self._set_pieces(agent=board.white, scaffold=self._get_scaffold(white_data))
        self._set_pieces(agent=board.black, scaffold=self._get_scaffold(black_data))

        return board

    # @classmethod
    # def from_pgn(
    #     cls,
    #     white_agent_cls: Type['Agent'],
    #     black_agent_cls: Type['Agent'],
    #     pgn: str,
    #     max_fullmoves: Optional[int] = 300,
    # ):
    #     processor = PGNProcessor(pgn=pgn)

    # TODO what if we want to load a partial game using PGN, then
    # play it out using RandomAgent? Currently there's no way to do this
    # We will have to play out the game using a "mock" ManualAgent, then
    # switch over to the real Agent. Or something like that

    #
    #     return cls(
    #         max_fullmoves=max_fullmoves,
    #         white=white_agent_cls.from_collection(
    #             color=constants.WHITE, coll=processor.white
    #         ),
    #         black=black_agent_cls.from_collection(
    #             color=constants.BLACK, coll=processor.black
    #         ),
    #         game_tree=processor.game_tree,
    #     )
