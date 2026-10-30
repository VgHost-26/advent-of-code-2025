import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = [
        (int(_range.split("-")[0]), int(_range.split("-")[1]))
        for _range in data.split("\n\n")[0].splitlines()
    ]
    products = [int(product) for product in data.split("\n\n")[1].splitlines()]
    return ranges, products


# % start
def part1(parsed) -> int:
    ranges, products = parsed
    good_products = 0
    for product in products:
        for _range in ranges:
            if product >= _range[0] and product <= _range[1]:
                good_products += 1
                break

    return good_products


# % end


def part2(parsed):
    # TODO: solve part 2
    return None


PARTS = {"1": part1, "2": None}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day05.txt")
