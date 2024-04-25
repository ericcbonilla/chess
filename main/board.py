from typing import List, Optional, Type

from main import constants
from main.exceptions import InvalidGameError
from main.game_tree import FullMove, HalfMove
from main.pieces import WhitePawn, BlackPawn, Rook, Knight, Bishop, Queen, King
from main.team import Team
from main.types import PieceType, Change, GameResult
from main.xposition import XPosition


class Board:
    """
    The highest-level object in our data model. Contains references to all
    pieces and prior moves. The board knows all.
    """

    def __init__(self):
        self.piece_counts = {
            'WHITE_ROOKS': 0,
            'BLACK_ROOKS': 0,
            'WHITE_KNIGHTS': 0,
            'BLACK_KNIGHTS': 0,
            'WHITE_BISHOPS': 0,
            'BLACK_BISHOPS': 0,
            'WHITE_QUEENS': 0,
            'BLACK_QUEENS': 0,
        }

        self.white = Team(color=constants.WHITE)
        self.black = Team(color=constants.BLACK)
        self.white_graveyard = Team(color=constants.WHITE)
        self.black_graveyard = Team(color=constants.BLACK)

        self.game_tree = FullMove()
        self.halfmove_clock = 0
        self.fullmove_number = 0
        self.result: GameResult = ''

    def __repr__(self) -> str:
        return (f'White:\n{self.white}\nWhite graveyard:\n{self.white_graveyard}\n'
                f'Black:\n{self.black}\nBlack graveyard:\n{self.black_graveyard}')

    # def team_to_play(self) -> Team:
    #     halfmove = self.game_tree.get_latest_halfmove()
    #     if halfmove and halfmove.color == constants.WHITE:
    #         return self.black
    #     else:
    #         return self.white

    @classmethod
    def from_fen(cls):
        # converter = FenConverter()
        # converter.to_board()

        pass

    def to_fen(self):
        # converter = FenConverter()
        # converter.from_board()

        pass

    @classmethod
    def from_pgn(cls):
        # Algebraic notation
        pass

    def to_pgn(self):
        pass

    # def _get_pawn_name(
    #     self,
    #     x: Optional[XPosition] = None,
    #     team: Optional[Team] = None,
    # ) -> str:
    #     pawn_name = f'{x.upper()}P'
    #
    #     def available(pn):
    #         return pn not in team
    #
    #     if available(pawn_name):
    #         return pawn_name
    #     else:
    #         new_x = x
    #         while not available(pawn_name):
    #             if new_x + 1:
    #                 new_x = new_x + 1
    #             else:
    #                 new_x = new_x - 1
    #             pawn_name = f'{new_x.upper()}P'
    #         return pawn_name

    def get_piece_name(
        self,
        piece_type: Type[PieceType],
        color: str,
        x: Optional[XPosition] = None,
        # team: Optional[Team] = None,
    ) -> str:
        if piece_type in (WhitePawn, BlackPawn) and x:
            # and team is not None:
            # TODO this will break if given a FEN position with 2+ pawns on the same column
            # This is a tough one so I'll come back to it later. Passing in team to this
            # method was breaking things for some reason.
            return f'{x.upper()}P'
            # return self._get_pawn_name(x, team)
        elif piece_type is Rook:
            count = self.piece_counts[f'{color}_ROOKS']
            return f'R{count + 1}'
        elif piece_type is Knight:
            count = self.piece_counts[f'{color}_KNIGHTS']
            return f'N{count + 1}'
        elif piece_type is Bishop:
            count = self.piece_counts[f'{color}_BISHOPS']
            return f'B{count + 1}'
        elif piece_type is Queen:
            count = self.piece_counts[f'{color}_QUEENS']
            return f'Q{count + 1}'
        elif piece_type is King:
            return 'K'

    def is_valid_position(self) -> bool:
        # TODO only really blatant stuff, like more than 8 pawns, 1 king
        # Same stuff that FEN would check for
        # If a team is in check, ensure it's that team's turn
        # Pawns cannot be on their back rank

        if not ('K' in self.white and 'K' in self.black):
            return False

        # team_to_play = self.team_to_play()
        # team_last_played = self.white if team_to_play is self.black else self.black
        # if team_last_played['K'].is_in_check():
        #     return False

        for team in (self.white, self.black):
            if len(team) > 16:
                return False

        return True

    def add_pieces(self, pieces: List[PieceType]):
        # TODO Order matters here. King from each team should come first
        # It'll make things most computationally efficient
        # TODO for FEN we must add pieces left to right, top to bottom

        for piece in pieces:
            self.add_piece(piece)

        if not self.is_valid_position():
            raise InvalidGameError("Invalid position")

    def add_piece(self, piece: PieceType, name: Optional[str] = None):
        piece.name = name or self.get_piece_name(type(piece), piece.team.color, piece.x)
        piece.team[piece.name] = piece

        piece_count_key = f'{piece.team.color}_{piece.__class__.__name__.upper()}S'
        if piece_count_key in self.piece_counts:
            self.piece_counts[piece_count_key] += 1

        graveyard = self.white_graveyard if piece.team.color == constants.WHITE else self.black_graveyard
        if piece.name in graveyard:
            del graveyard[piece.name]

    def destroy_piece(self, piece: PieceType):
        piece_count_key = f'{piece.team.color}_{piece.__class__.__name__.upper()}S'
        if piece_count_key in self.piece_counts:
            self.piece_counts[piece_count_key] -= 1

        if piece.team.color == constants.WHITE:
            self.white_graveyard[piece.name] = piece
        else:
            self.black_graveyard[piece.name] = piece

        del piece.team[piece.name]

    def apply_change(self, change: Change):
        """
        All game state changes (i.e. changes to Teams and Pieces) should happen
        here. State should never be changed from anywhere else.
        """

        for team in (self.white, self.black):
            if change[team.color]:
                for key, datum in change[team.color].items():
                    if key == 'en_passant_target':
                        team.en_passant_target = datum[1]
                        continue

                    if datum['new_position'] is None:
                        piece = team[key]
                        self.destroy_piece(piece)
                    elif datum['old_position'] is None:
                        # We're either resurrecting a piece, or promoting a pawn
                        x, y = datum['new_position']
                        piece = datum['piece_type'](
                            board=self,
                            team=team,
                            x=XPosition(x),
                            y=y,
                        )
                        self.add_piece(piece, name=key)
                    else:
                        x, y = datum['new_position']
                        piece = team[key]
                        piece.x, piece.y = XPosition(x), y

                    if 'has_moved' in datum:
                        piece.has_moved = datum['has_moved']

        if 'game_result' in change and change['game_result']:
            # TODO if the game is over, use this to prevent further moves
            self.result = change['game_result']

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
        inverted_change = {
            constants.WHITE: {},
            constants.BLACK: {},
        }

        for color in constants.COLORS:
            if halfmove.change[color]:
                for key, datum in halfmove.change[color].items():
                    if key == 'en_passant_target':
                        inverted_change[color][key] = (datum[1], datum[0])
                        continue

                    inverted_change[color][key] = {
                        'old_position': datum['new_position'],
                        'new_position': datum['old_position'],
                    }

                    graveyard = self.white_graveyard if color == constants.WHITE else self.black_graveyard
                    if key in graveyard:
                        inverted_change[color][key]['piece_type'] = type(graveyard[key])
                    if 'has_moved' in datum:
                        inverted_change[color][key]['has_moved'] = not datum['has_moved']

        self.apply_change(inverted_change)
        self.game_tree.prune()
