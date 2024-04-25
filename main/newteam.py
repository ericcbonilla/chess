from typing import Optional, Set

from main.types import Position, TeamColor

"""
4/24/24

Potential for a pretty big refactor for how Teams work. Instead of extending Dict,
just make Team a custom class with defined slots for each piece. We will also need 8
extra slots for potential promotions. It's a lot, but it's still a relatively
low number of class attributes. Some other thoughts:

- Instead of having 8 extra slots for potential promotions, we could just have 16
slots total. You would just replace the pawn with the promoted piece, under the
same slot.

- With pieces as well defined attributes, game state can also be implicitly
validated. For instance, king will be a required attribute, while a_rook is not.
We could get rid of most or all of Board.is_valid_position?
- Except that wouldn't work for graveyards...we'd have to make all attributes optional

- Safer, faster data access. We access a piece via a defined attribute instead of
a computed name str.

- Also would remove the need for piece naming and counting, which has been a
pretty big hassle, especially when dealing with positions with more than 2 of a
piece type, or positions with multiple pawns (of a color) on the same file

- We'd still need to compute piece assignment though. Dark bishop, light bishop.
Pawns would be assigned based on their file. If we're given two or more pawns on
the same file, assign each pawn to the next available slot?

- But without given names, how would we reference a piece during manual play?
By position? Or by just knowing which attribute to access for each piece?

- We'd still need to be able to iterate over Team values. Make sure this is
not an antipattern when using slots
"""


class NewTeam:
    piece_names = (
        # If additional pieces are provided, assign them to any empty pawn slots
        "a_pawn",
        "b_pawn",
        "c_pawn",
        "d_pawn",
        "e_pawn",
        "f_pawn",
        "g_pawn",
        "h_pawn",
        # Would these names be problematic down the road? How would we pick
        # which slot to assign a piece to given a midgame position? Would it
        # even matter?
        "a_rook",
        "h_rook",
        "b_knight",
        "g_knight",
        "dark_bishop",
        "light_bishop",
        "queen",
        "king",
    )
    __slots__ = ("color", "en_passant_target") + piece_names

    def __init__(self, color: TeamColor, en_passant_target: Optional[Position] = None):
        self.color = color
        self.en_passant_target = en_passant_target

    @property
    def pieces(self):
        for name in self.piece_names:
            if hasattr(self, name):
                yield getattr(self, name)

    @property
    def positions(self) -> Set[Position]:
        return set(piece.position for piece in self.pieces)
