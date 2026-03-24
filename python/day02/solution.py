import sys
import os


def solve():
    # Read input
    input_file = "inputs\day02.txt"
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
        start_str = r["from"]
        end = int(r["to"])
        end_str = r["to"]

        
        while len(start_str) < len(end_str) + 1: 
            # print(f'start_str {start_str} end_str {end_str}')
        
            if (len(start_str) == len(end_str)) and (len(start_str) % 2 != 0):
                # print(f'skipping {r}')
                break
            
            if len(start_str) % 2 == 0:
                half_len = len(start_str) // 2
                left = start_str[:half_len]
                right = left
                id = left + right

                for i in range(half_len):
                    if start < int(id) < end:
                        sum += int(id)
                        print(f'add {id}')
                    else:
                        break
                    left = list(left)
                    right = list(right)
                    left[(half_len - 1) - i] = str(int(left[(half_len - 1) - i]) + 1)
                    right[(half_len - 1) - i] = str(int(right[(half_len - 1) - i]) + 1)
                    id = ''.join(left) + ''.join(right)
            
            start_str = '1' + '0' * len(start_str)
            start = int(start_str)

    print(f"Part I final sum: {sum}")
    exit()

    # Part 2

    sum = 0
    for r in ranges:
        start = int(r["from"])
        end = int(r["to"])

        for id in range(start, end + 1):
            id_str = str(id)
            id_length = len(id_str)

            for i in range(1, (id_length // 2) + 1):
                pattern = id_str[:i]
                pattern_count = id_str.count(pattern)

                if pattern_count == 1:
                    break

                if pattern_count == id_length / i:
                    sum += id
                    print(id)
                    break

    print(f"Part II final sum: {sum}")

    # % end


if __name__ == "__main__":
    solve()
