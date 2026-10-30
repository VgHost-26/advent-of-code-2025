import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> list[str]:
    return data.splitlines()


# % start
def part1(lines: list[str]) -> int:

    current_position = 50
    pointed_at_zero = 0
    for line in lines:
        direction = line[0]
        distance = int(line[1:])

        if direction == "R":
            current_position = (current_position + distance) % 100
        elif direction == "L":
            current_position = (current_position - distance) % 100

        if current_position == 0:
            pointed_at_zero += 1

    # print(f"Part I password: {pointed_at_zero}")
    return pointed_at_zero
# % end


# % start
def part2(lines: list[str]) -> int:

    current_position = 50
    pointed_at_zero = 0

    current_position = 50
    pointed_at_zero = 0
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        multiple_passes = 0
        # print(f"Dial turn [{line}] to pos ", end='')

        if direction == "R":
            overflow = current_position + distance
            multiple_passes = overflow // 100
            current_position = (current_position + distance) % 100

        elif direction == "L":
            overflow = current_position - distance
            multiple_passes = abs(overflow // 100)
            if current_position == 0:
                multiple_passes -= 1
            current_position = (current_position - distance) % 100

        # print(f"{current_position}")
        if current_position == 0:
            pointed_at_zero += 1
            multiple_passes -= 1
            # print(f"added exactly pointing at zero: [{line}]")
        if multiple_passes > 0:
            pointed_at_zero += multiple_passes
            # print(f"added multiple rounds: [{line}]  {multiple_passes}")
    return pointed_at_zero

# % end


# % start
def part2_brute(parsed) -> int:
    current_position = 50
    pointed_at_zero = 0
    for line in parsed:
        direction = line[0]
        distance = int(line[1:])

        if direction == "R":
            for _ in range(distance):
                current_position += 1
                if current_position == 100:
                    pointed_at_zero += 1
                    current_position = 0
                if current_position > 100:
                    current_position = 1

        if direction == "L":
            for _ in range(distance):
                current_position -= 1
                if current_position == 0:
                    pointed_at_zero += 1
                    current_position = 100
                if current_position < 0:
                    current_position = 99
    return pointed_at_zero
# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day01.txt")
