import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> list[str]:
    return data.splitlines()


# % start
def part1(lines: list[str]) -> int:
    lines = [list(filter(None, line.split(" "))) for line in lines]  # type: ignore
    columns = zip(*lines)

    total_sum = 0
    for col in columns:
        operation = col[len(col) - 1]

        col_result = 0
        if operation == "+":
            col_result = 0
            for i in range(len(col) - 1):
                col_result += int(col[i])

        if operation == "*":
            col_result = 1
            for i in range(len(col) - 1):
                col_result *= int(col[i])

        total_sum += col_result
    return total_sum


# % end


# % start
def part2(lines: list[str]) -> int:
    matrix = zip(*lines)

    symbol = ""
    total_sum = 0
    result = 0
    nums = [""]
    list_matrix = list(matrix)
    list_matrix.reverse()

    for _i, line in enumerate(list_matrix):
        for item in line:
            if item.isdigit():
                nums[len(nums) - 1] += item

        if line[len(line) - 1] in ["+", "*"]:
            symbol = line[len(line) - 1]
            result = 0 if symbol == "+" else 1

            for num in nums:
                if not num.isdigit():
                    continue
                if symbol == "+":
                    result += int(num)
                else:
                    result *= int(num)
            total_sum += result

            nums = [""]
            result = 0 if symbol == "+" else 1
        else:
            nums.append("")
    return total_sum


# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day06.txt")
