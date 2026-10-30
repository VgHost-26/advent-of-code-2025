import os
import sys
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402

MASK = [
    (-1, -1),
    (-1, 0),
    (-1, +1),
    (0, -1),
    #
    (0, +1),
    (+1, -1),
    (+1, 0),
    (+1, +1),
]


def parse(data: str) -> list[list[str]]:
    return [list(line) for line in data.splitlines()]


# % start
def _removable(grid: list[list[str]]) -> int:
    width = len(grid[0])
    height = len(grid)
    count_removed = 0
    for i, line in enumerate(grid):
        for j, field in enumerate(line):
            if field == "@":
                count = 0
                for m in MASK:
                    if (
                        i + m[0] >= height
                        or i + m[0] < 0
                        or j + m[1] >= width
                        or j + m[1] < 0
                    ):
                        continue
                    if grid[i + m[0]][j + m[1]] == "@":
                        count += 1
                    if count > 4:
                        break
                if count < 4:
                    count_removed += 1
    return count_removed


def part1(grid: list[list[str]]) -> int:
    to_remove = _removable(grid)
    return to_remove


# % end


# % start
def part2(grid: list[list[str]]) -> int:
    grid = deepcopy(grid)
    width = len(grid[0])
    height = len(grid)
    total_removed = 0
    to_remove = _removable(grid)
    while to_remove != 0:
        to_remove = 0
        for i, line in enumerate(grid):
            for j, field in enumerate(line):
                if field == "@":
                    count = 0
                    for m in MASK:
                        if (
                            i + m[0] >= height
                            or i + m[0] < 0
                            or j + m[1] >= width
                            or j + m[1] < 0
                        ):
                            continue
                        if grid[i + m[0]][j + m[1]] == "@":
                            count += 1
                        if count > 4:
                            break
                    if count < 4:
                        grid[i][j] = "."
                        to_remove += 1

        total_removed += to_remove
    return total_removed


# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day04.txt")
