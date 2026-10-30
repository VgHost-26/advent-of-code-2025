import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> list[str]:
    data_array = [line for line in data.splitlines()]
    if data_array[0][len(data_array[0]) // 2] != "S":
        raise Exception("Middle is not a starting point")  # noqa: TRY002
    return data_array


# % start
def part1(data_array: list[str]) -> int:
    height = len(data_array)
    middle = len(data_array[0]) // 2

    splits = 0
    flows = [middle]

    for level in range(1, height):
        row = data_array[level]
        offset = 0

        while row.find("^", offset) != -1:
            splitter_pos = row.find("^", offset)
            offset = splitter_pos + 1

            if splitter_pos in flows:
                splits += 1
                flows.remove(splitter_pos)
                if flows.count(splitter_pos + 1) == 0:
                    flows.append(splitter_pos + 1)
                if flows.count(splitter_pos - 1) == 0:
                    flows.append(splitter_pos - 1)
    return splits
# % end


# % start
def part2(data_array: list[str]) -> int:
    height = len(data_array)
    middle = len(data_array[0]) // 2

    current_paths = {middle: 1}
    for level in range(1, height):
        row = data_array[level]
        next_paths = {}

        for pos, count in current_paths.items():
            if row[pos] == "^":
                next_paths[pos + 1] = next_paths.get(pos + 1, 0) + count
                next_paths[pos - 1] = next_paths.get(pos - 1, 0) + count
            else:
                next_paths[pos] = next_paths.get(pos, 0) + count

        current_paths = next_paths

    timelines = sum(current_paths.values())
    return timelines
# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day07.txt")
