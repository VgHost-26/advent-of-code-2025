# AoC solution template -- parts as pure functions; bench via `--bench` (BENCH-PLAN.md)
# % unsolved
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str):
    """Raw input text -> shared problem data (parts must not mutate it)."""
    # TODO: adjust based on input type
    return data


# % start
def part1(parsed) -> int:
    # TODO: solve part 1
    return 0
# % end


# % start
def part2(parsed) -> int:
    # TODO: solve part 2
    return 0
# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day{DAY2}.txt")
