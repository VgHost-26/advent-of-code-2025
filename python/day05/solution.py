import sys

def solve():
    # Read input
    input_file = "inputs/day05.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(input_file, "r") as f:
        data = f.read().strip()

    print(f"Solving with input from {input_file}")
    # Part 1
    # ...

#     data = """3-5
# 10-14
# 16-20
# 12-18

# 1
# 5
# 8
# 11
# 17
# 32"""

    ranges = [
        (int(range.split("-")[0]), int(range.split("-")[1]))
        for range in data.split("\n\n")[0].splitlines()
    ]
    products = [int(product) for product in data.split("\n\n")[1].splitlines()]

    # print(ranges)
    # print(products)

    good_products = 0
    for product in products:
        for _range in ranges:
            if product >= _range[0] and product <= _range[1]:
                good_products += 1
                break 
                

    print("Total good products: ", good_products)



    # Part 2
    # ...

if __name__ == "__main__":
    solve()
