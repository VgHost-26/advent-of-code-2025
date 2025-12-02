import sys
import os

def solve():
    # Read input
    input_file = "inputs/day01.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    with open(input_file, 'r') as f:
        data = f.read().strip()
    
    print(f"Solving with input from {input_file}")
    #% Part 1
    
    current_position = 50
    pointed_at_zero = 0
    for line in data.splitlines():
        direction = line[0]
        distance = int(line[1:])
        
        if direction == "R":
            current_position = (current_position + distance) % 100
        elif direction == "L":
            current_position = (current_position - distance) % 100
        
        if current_position == 0:
            pointed_at_zero += 1
    
    print(f"Part I password: {pointed_at_zero}")
    
    #%   
         
    #% Part 2
    
    
    
    #%
    
if __name__ == "__main__":
    solve()
