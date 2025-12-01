import sys
import os

def solve():
    # Read input
    input_file = "input.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    with open(input_file, 'r') as f:
        data = f.read().strip()
    
    print(f"Solving with input from {input_file}")
    # Part 1
    # ...
    
    # Part 2
    # ...

if __name__ == "__main__":
    solve()
