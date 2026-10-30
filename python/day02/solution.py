import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> list[tuple[int, int]]:
    ranges = []
    for r in data.split(","):
        lo, hi = r.split("-", 2)
        ranges.append((int(lo), int(hi)))
    return ranges



# % start
def part1(ranges: list[tuple[int, int]]) -> int:

    total = 0
    for start, end in ranges:
        start_str = str(start)
        end_str = str(end)

        while len(start_str) < len(end_str) + 1:
            if (len(start_str) == len(end_str)) and (len(start_str) % 2 != 0):
                break

            if len(start_str) % 2 == 0:
                half_len = len(start_str) // 2
                left = start_str[:half_len]
                right = left
                id = left + right

                for i in range(half_len):
                    if start < int(id) < end:
                        total += int(id)
                    else:
                        break
                    left = list(left)
                    right = list(right)
                    left[(half_len - 1) - i] = str(int(left[(half_len - 1) - i]) + 1)
                    right[(half_len - 1) - i] = str(int(right[(half_len - 1) - i]) + 1)
                    id = "".join(left) + "".join(right)

            start_str = "1" + "0" * len(start_str)
            start = int(start_str)

    return total
# % end



# % start
def part2(ranges: list[tuple[int, int]]) -> int:
    total = 0
    for lo, hi in ranges:
        for id_ in range(lo, hi + 1):
            id_str = str(id_)
            id_length = len(id_str)

            for i in range(1, (id_length // 2) + 1):
                pattern = id_str[:i]
                pattern_count = id_str.count(pattern)

                if pattern_count == 1:
                    break

                if pattern_count == id_length / i:
                    total += id_
                    break
    return total
# % end



PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day02.txt")
