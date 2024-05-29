from dataclasses import dataclass

from main.types import AgentColor, Change


@dataclass
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

        # These last three items are only ever used to generate algebraic notation;
        # there are no state changes made based on these values
        'disambiguation': '',
        'check': False,
        'game_result': None,
    }
    """

    color: AgentColor
    change: Change

    def to_an(self) -> str:
        # TODO do we want this to be baked into the Change? Or generated after
        # the fact?
        pass
