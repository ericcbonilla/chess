from main.agents import ManualAgent
from main.pieces import King, Queen, WhitePawn


class TestBoardBuilder:
    def test_added_pawn_has_correct_name(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": WhitePawn, "x": "f", "y": 2},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        assert board.white.f_pawn

    def test_second_added_queen_has_correct_name(self, builder):
        board = builder.from_data(
            white_agent_cls=ManualAgent,
            black_agent_cls=ManualAgent,
            white_data=[
                {"piece_type": King, "x": "c", "y": 4},
                {"piece_type": Queen, "x": "g", "y": 5},
                {"piece_type": Queen, "x": "g", "y": 4},
                {"piece_type": Queen, "x": "g", "y": 3},
            ],
            black_data=[
                {"piece_type": King, "x": "e", "y": 5},
            ],
        )

        assert board.white.queen.position == ("g", 5)
        assert board.white.g_prom.position == ("g", 4)
        assert board.white.h_prom.position == ("g", 3)

    # TODO
    # def test_multiple_pawns_on_same_column_have_correct_names(self):
    #     board = Board()
    #     board.add_pieces([
    #         King(board=board, agent=board.white, x='c', y=4),
    #         King(board=board, agent=board.black, x='e', y=5),
    #         BlackPawn(board=board, agent=board.black, x='e', y=7),
    #         BlackPawn(board=board, agent=board.black, x='e', y=6),
    #     ])
    #
    #     assert 'EP' in board.black
    #     assert 'FP' in board.black
