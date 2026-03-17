from copy import deepcopy
import sys
import os


def solve():
    # Read input
    input_file = "inputs/day04.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(input_file, "r") as f:
        data = f.read().strip()

    print(f"Solving with input from {input_file}")

#     data = """..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@."""

    # Part 1
    grid = [list(line) for line in data.splitlines()]
    print(grid[1][0])
    mask = [
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

    to_remove = 0
    width = len(grid[0])
    height = len(grid)
    preview = deepcopy(grid)
    
    for i, line in enumerate(grid):
        for j, field in enumerate(line):
            if field == "@":
                count = 0
                for m in mask:
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
                    preview[i][j] = f'{count}'
                    to_remove += 1
    print("total: ", to_remove)
    # for line in preview:
        # print("".join(line))
        
        
    
    # Part 2
    total_removed = 0
    while to_remove != 0:
        to_remove = 0
        for i, line in enumerate(grid):
            for j, field in enumerate(line):
                if field == "@":
                    count = 0
                    for m in mask:
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
                        grid[i][j] = '.'
                        to_remove += 1
   
        total_removed += to_remove
        print("to remove: ", to_remove)
        # for line in grid:
        #     print("".join(line))
            
    print(total_removed)

if __name__ == "__main__":
    solve()
