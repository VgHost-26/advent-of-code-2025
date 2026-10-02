import os
import sys


def solve():
    # Read input
    input_file = "inputs/day07.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    with open(input_file, 'r') as f:
        data = f.read().strip()
    
    
#     data = '''.......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ...............'''
    
    print(f"Solving with input from {input_file}")
    # % start
    # Part 1
    
    data_array = [line for line in data.splitlines()]
    height = len(data_array)
    width = len(data_array[0])
    middle = width // 2
    
    
    if (data_array[0][middle] != 'S'):
        raise Exception('Middle is not a starting point')  # noqa: TRY002
    
    splits = 0
    flows = [middle]
    
    for level in range(1, height):
        row = data_array[level]
        offset = 0
        
        while row.find('^', offset) != -1:
            splitter_pos = row.find('^', offset)
            offset = splitter_pos + 1

            if splitter_pos in flows:
                splits += 1
                flows.remove(splitter_pos)
                if flows.count(splitter_pos + 1) == 0: flows.append(splitter_pos + 1)    
                if flows.count(splitter_pos - 1) == 0: flows.append(splitter_pos - 1)    
                
    print('splits: ', splits)
    
    
    # Part 2
    
    current_paths = {middle:1}
    for level in range(1, height):
        row = data_array[level]
        next_paths = {}

        for pos, count in current_paths.items():
            if row[pos] == '^':
                next_paths[pos + 1] = next_paths.get(pos + 1, 0) + count
                next_paths[pos - 1] = next_paths.get(pos - 1, 0) + count
            else:
                next_paths[pos] = next_paths.get(pos, 0) + count

        current_paths = next_paths
        
    timelines = sum(current_paths.values())
    
    # % end

    # def new_path(starting_level, position):
    #     _current_level = starting_level
    #     _timelines = 0
        
    #     while _current_level < height:
    #         _row = data_array[_current_level]

    #         if _row[position] == '^':
    #             _timelines += new_path(_current_level + 1, position + 1)
    #             _timelines += new_path(_current_level + 1, position - 1)
    #             return _timelines
    #         else:
    #             _current_level += 1

    #     return 1
    # timelines = new_path(starting_level=1, position=middle)
         
    print('timelines: ', timelines)

if __name__ == "__main__":
    solve()
