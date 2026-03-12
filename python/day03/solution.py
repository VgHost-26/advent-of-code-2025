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

  

if __name__ == "__main__":
    solve()
