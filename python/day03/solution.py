from copy import deepcopy
import sys
import os


def solve():
    # Read input
    input_file = "inputs/day03.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(input_file, "r") as f:
        data = f.read().strip()

    print(f"Solving with input from {input_file}")
    # Part 1
    # ...

#     data = """987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """

    # print(data)
    
    banks = data.split()
    banks_list = []
    for bank in banks:
        arr = [int(char) for char in bank]
        banks_list.append(arr)

    import copy

    banks_list_2 = copy.deepcopy(banks_list)
    # print(banks_list)
    total_juice = 0
    for bank in banks_list:
        # print(f"bank: {bank}")
        max1 = max(bank)
        max1_i = bank.index(max1)

        last = False
        if max1_i != len(bank) - 1:
            bank = bank[max1_i + 1 :]
        else:
            bank.pop()
            last = True

        max2 = max(bank)
        max2_i = bank.index(max2)

        # juice = f"{max1}{max2}" if max1_i < max2_i else f"{max2}{max1}"
        juice = f"{max1}{max2}" if not last else f"{max2}{max1}"
        # print(f"juice: {juice}")
        total_juice += int(juice)

    print(total_juice)
    # Part 2
    # ...

    import numpy as np

    sum = 0

    def get_all_indexes(arr, x):
        return [i for i, el in enumerate(arr) if el == x]

    def list_to_int(arr):
        _arr = deepcopy(arr)
        _output = [str(int(o)) for o in _arr if o != 0]
        _output = "".join(_output)
        if _output == "":
            return 0
        return int(_output)

    def find_spot(output, number, poss):
        curr_max = list_to_int(output)
        sel_i = 0
        for pos in poss:
            test_out = deepcopy(output)
            test_out[pos] = number
            if list_to_int(test_out) > curr_max:
                curr_max = list_to_int(test_out)
                sel_i = pos
        output[sel_i] = number
        return output, sel_i

    for bank in banks_list_2:
        output = np.zeros(len(bank))
        lasts = 1
        for i in range(12):
            m = max(bank)
            mi = get_all_indexes(bank, m)
            if len(mi) == 1:
                output[mi] = m
                mi = mi[0]
            else:
                output, mi = find_spot(output=output, number=m, poss=mi)

            if mi == len(bank) - lasts:
                bank[mi] = 0
                lasts += 1

            elif mi > 0 and max(output[:mi]) < m and len(bank[mi:]) >= 12:
                bank = list(np.zeros(mi + 1)) + bank[mi + 1 :]
            else:
                bank[mi] = 0
        output = [str(int(o)) for o in output if o != 0]
        output = "".join(output)
        print(output)
        sum += int(output)

    print(sum)


if __name__ == "__main__":
    solve()
