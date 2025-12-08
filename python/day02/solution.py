import sys

def solve():
    # Read input
    input_file = "inputs/day02.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(input_file, "r") as f:
        data = f.read().strip()

    print(f"Solving with input from {input_file}")
    # % start
    # Part 1

    raw_ranges = data.split(",")
    ranges = []
    for r in raw_ranges:
        f, t = r.split("-", 2)
        ranges.append({"from": f, "to": t})

    sum = 0
    for r in ranges:
        start = int(r["from"])
        end = int(r["to"])
        
        for id in range(start, end + 1):
            id_str = str(id)
            id_length = len(id_str)
            
            if id_length % 2 != 0:
                continue
            
            left = id_str[:id_length//2]
            right = id_str[id_length//2:]
            
            if left == right:
                sum += id
                
            # print(f"{id} --- left: {left} | right: {right}")
        
    print(f"Part I final sum: {sum}")
    
    # Part 2
    
    sum = 0
    for r in ranges:
        start = int(r["from"])
        end = int(r["to"])
        
        for id in range(start, end + 1):
            id_str = str(id)
            id_length = len(id_str)
            
            for i in range(1, (id_length//2) + 1):
                pattern = id_str[:i]
                pattern_count = id_str.count(pattern)
                
                if pattern_count == 1:
                    break
                
                if pattern_count == id_length/i:
                    sum += id
                    print(id)
                    break
     
            
            
    print(f"Part II final sum: {sum}")
    
    
    # % end


if __name__ == "__main__":
    solve()
