import sys

def solve():
    # Read input
    input_file = "inputs/day01.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    with open(input_file, 'r') as f:
        data = f.read().strip()
    
    print(f"Solving with input from {input_file}")
    
    # % start
    # Part 1
    print("Part 1: Solution")
    
    
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
    
    # Part 2
    print("Part 2: Solution")
    
    
    current_position = 50
    pointed_at_zero = 0

    
    current_position = 50
    pointed_at_zero = 0
    for line in data.splitlines():
        direction = line[0]
        distance = int(line[1:])
        multiple_passes = 0
        # print(f"Dial turn [{line}] to pos ", end='')
        
        if direction == "R":
            overflow = current_position + distance
            multiple_passes = overflow // 100
            current_position = (current_position + distance) % 100
            
        elif direction == "L":
            overflow = current_position - distance
            multiple_passes = abs(overflow // 100)
            if current_position == 0:
                multiple_passes -= 1 
            current_position = (current_position - distance) % 100
        
        
        # print(f"{current_position}")
        if current_position == 0:
            pointed_at_zero += 1
            multiple_passes -= 1
            # print(f"added exactly pointing at zero: [{line}]")
        if multiple_passes > 0:
            pointed_at_zero += multiple_passes
            # print(f"added multiple rounds: [{line}]  {multiple_passes}")
        
    print(f"Part II password: {pointed_at_zero}")
    bruteforce_part2(data)
        
    # % end


def bruteforce_part2(data):
    current_position = 50
    pointed_at_zero = 0

    for line in data.splitlines():
        direction = line[0]
        distance = int(line[1:])
        
        if direction == 'R':
            for i in range(distance):
                current_position += 1
                if current_position == 100:
                    pointed_at_zero +=1
                    current_position = 0
                if current_position > 100:
                    current_position = 1
        
        if direction == 'L':
            for i in range(distance):
                current_position -= 1
                if current_position == 0:
                    pointed_at_zero +=1
                    current_position = 100
                if current_position < 0:
                    current_position = 99
                    
    print("Bruteforce part 2:", pointed_at_zero)
    return pointed_at_zero
    
if __name__ == "__main__":
    solve()
 