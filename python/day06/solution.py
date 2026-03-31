import sys
import os


def solve():
    # Read input
    input_file = "inputs/day06.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(input_file, "r") as f:
        data = f.read()

    print(f"Solving with input from {input_file}")

#     data = """123 328  51 64 
#  45 64  387 23 
#   6 98  215 314
# *   +   *   +  """

    # Part 1
    # ...

    lines = data.splitlines()
    lines = [list(filter(None, line.split(" "))) for line in lines]
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

    print(total_sum)
    # Part 2
    # ...

    lines = data.splitlines()
    matrix = zip(*lines)

  

    symbol = ""
    total_sum = 0
    result = 0
    nums = [""]
    list_matrix = list(matrix)
    list_matrix.reverse()
        
    for i, line in enumerate(list_matrix):
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
            print(nums, f"{symbol}=", result)

            nums = [""]
            result = 0 if symbol == "+" else 1
        else:
            nums.append("")

    print(total_sum)


if __name__ == "__main__":
    solve()
