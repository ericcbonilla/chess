import statistics
import time

from colorist import green, red

from main.agents import AggressiveAgent, RandomAgent
from main.builders import BoardBuilder

BENCHMARK = 0.23
games_played = 0
times_per_halfmove = []

print("\nBenchmarking...")
while games_played <= 99:
    builder = BoardBuilder()
    board = builder.from_start(
        white_agent_cls=RandomAgent,
        black_agent_cls=AggressiveAgent,
        max_fullmoves=300,
    )

    start = time.perf_counter()
    board.play(internal=True)
    end = time.perf_counter()
    elapsed = end - start

    times_per_halfmove.append((elapsed / (board.fullmove_number * 2)) * 1000)
    games_played += 1

mean = statistics.mean(times_per_halfmove)
print(f"{games_played} games played. Mean time (ms) per halfmove: {mean}")

if mean > BENCHMARK:
    red(f"Fails benchmark of {BENCHMARK}")
else:
    green(f"Satisfies benchmark of {BENCHMARK}")
