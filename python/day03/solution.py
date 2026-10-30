import os
import sys
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import run_cli  # noqa: E402


def parse(data: str) -> list[list[int]]:
    return [[int(char) for char in bank] for bank in data.split()]
# % unsolved


# % start
def part1(banks: list[list[int]]) -> int:
    total_juice = 0
    for original in banks:
        bank = list(original)
        max1 = max(bank)
        max1_i = bank.index(max1)

        last = False
        if max1_i != len(bank) - 1:
            bank = bank[max1_i + 1:]
        else:
            bank.pop()
            last = True

        max2 = max(bank)
        max2_i = bank.index(max2)

        juice = f"{max1}{max2}" if not last else f"{max2}{max1}"
        total_juice += int(juice)
    return total_juice
# % end


# % start
def _get_all_indexes(arr, x):
    return [i for i, el in enumerate(arr) if el == x]


def _list_to_int(arr) -> int:
    _arr = deepcopy(arr)
    _output = [str(int(o)) for o in _arr if o != 0]
    _output = "".join(_output)
    if _output == "":
        return 0
    return int(_output)


def _find_spot(output, number, poss):
    curr_max = _list_to_int(output)
    sel_i = 0
    for pos in poss:
        test_out = deepcopy(output)
        test_out[pos] = number
        if _list_to_int(test_out) > curr_max:
            curr_max = _list_to_int(test_out)
            sel_i = pos
    output[sel_i] = number
    return output, sel_i


def part2(banks: list[list[int]]) -> int:
    sum_ = 0
    banks = deepcopy(banks)

    for bank in banks:
        output = [0] * len(bank)
        lasts = 1
        for _ in range(12):
            m = max(bank)
            mi = _get_all_indexes(bank, m)
            if len(mi) == 1:
                output[mi[0]] = m
                mi = mi[0]
            else:
                output, mi = _find_spot(output=output, number=m, poss=mi)

            if mi == len(bank) - lasts:
                bank[mi] = 0
                lasts += 1

            elif mi > 0 and max(output[:mi]) < m and len(bank[mi:]) >= 12:
                bank = [0] * (mi + 1) + bank[mi + 1:]
            else:
                bank[mi] = 0
        output_digits = [str(o) for o in output if o != 0]
        output_joined = "".join(output_digits)
        sum_ += int(output_joined)
    return sum_
# % end


PARTS = {"1": part1, "2": part2}

if __name__ == "__main__":
    run_cli(parse, PARTS, "inputs/day03.txt")
