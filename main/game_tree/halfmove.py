from dataclasses import dataclass

from main.types import AgentColor, Change
from main.x import to_str


@dataclass(slots=True)
class HalfMove:
    """
    Contains all the necessary information to:
    - Generate algebraic notation for this move
    - Show the exact state changes that occurred due to this move
    - Reverse those changes if we want to rollback this move

    The general shape of the change dict is shown in the example below.

    {
        # We will always have two items, represented as dicts, for each Agent. If
        # no change needs to be made for an Agent, the dict will be empty.
        constants.WHITE: {
            # Denotes a rook moving
            'R1': {
                'old_position': ('a', 1),
                'new_position': ('a', 3),

                # Only for Kings and Rooks. Used to compute castle legality
                'has_moved': True,
            }
        },
        constants.BLACK: {
            # Denotes an en passant target expiring
            'en_passant_target': (('d', 6), None),

            # Denotes a pawn being captured
            'DP': {
                'old_position': ('d', 5),
                'new_position': None,
            }
        },

        # These items are only ever used to generate algebraic notation;
        # there are no state changes made based on these values
        'disambiguation': '',
        'check': False,
        'game_result': None,
        'symbol': 'R',

        # Used to decide if the game is drawn based on the Seventy-five-move rule
        "halfmove_clock": (0, 0),

        # Used only for the arbiter to track the number of elapsed moves
        "fullmove_number": (1, 2),

        # Stored with each Halfmove so we can jump into the game at any point
        "fen": "rnbqkbnr/pppp1p1p/4P1p1/8/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 3",
    }
    """

    color: AgentColor
    change: Change

    @property
    def opponent_color(self) -> AgentColor:
        return "BLACK" if self.color == "WHITE" else "WHITE"

    @property
    def new_position(self) -> str:
        pc = [pc for pc in self.change[self.color].values() if pc["new_position"]][0]
        x, y = pc["new_position"]

        return f"{to_str(x)}{str(y)}"

    @property
    def mate_notation(self) -> str:
        if self.change["check"]:
            if self.change["game_result"] in ["1-0", "0-1"]:
                return "#"
            return "+"
        return ""

    @property
    def castle_notation(self) -> str:
        if "king" in self.change[self.color]:
            if "h_rook" in self.change[self.color]:
                return "O-O"
            elif "a_rook" in self.change[self.color]:
                return "O-O-O"
        return ""

    @property
    def promotion_notation(self) -> str:
        if self.change["symbol"] == "":
            if slots := [sl for sl in iter(self.change[self.color]) if "prom" in sl]:
                return f"={self.change[self.color][slots[0]]['piece_type'].symbol}"

        return ""

    @property
    def capture_notation(self) -> str:
        piece_death = self.change[self.opponent_color] and not (
            "en_passant_target" in self.change[self.opponent_color]
            and len(self.change[self.opponent_color]) == 1
        )
        return "x" if self.change[self.color] and piece_death else ""

    @property
    def symbol(self) -> str:
        if self.capture_notation and self.change["symbol"] == "":
            pawn_slot = [sl for sl in iter(self.change[self.color]) if "pawn" in sl][0]
            x, _ = self.change[self.color][pawn_slot]["old_position"]
            return to_str(x)

        return self.change["symbol"]

    def to_an(self) -> str:
        if self.castle_notation:
            return f"{self.castle_notation}{self.mate_notation}"

        return (
            f"{self.symbol}"
            f"{self.change['disambiguation']}"
            f"{self.capture_notation}"
            f"{self.new_position}"
            f"{self.promotion_notation}"
            f"{self.mate_notation}"
        )
