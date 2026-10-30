package main

import (
	"slices"
	"strconv"
	"strings"

	aoc "advent-of-code-2025"
	"math"
	"os"
)

type Range struct {
	Start int
	End   int
}

func ceilDiv(a, b int) int {
	return (a + b - 1) / b
}

func parse(data string) []Range {
	var rangesNumbers []Range

	for _, pair := range strings.Split(data, ",") {
		first, second, found := strings.Cut(pair, "-")
		if !found {
			panic("error while splitting")
		}
		firstInt, err := strconv.Atoi(first)
		if err != nil {
			panic(err)
		}
		secondInt, err := strconv.Atoi(second)
		if err != nil {
			panic(err)
		}
		rangesNumbers = append(rangesNumbers, Range{firstInt, secondInt})
	}

	return rangesNumbers
}

// % start
func part1_hmm(rangesNumbers []Range) int {
	invalidSum := 0

	for _, r := range rangesNumbers {
		for half := 1; half <= (len(strconv.Itoa(r.End))+1)/2; half++ {
			base := int(math.Pow10(half))
			leftLo := 1
			if half > 1 {
				leftLo = base / 10
			}
			startLeft := max(leftLo, (r.Start+base)/(base+1))
			endLeft := min(base-1, r.End/(base+1))

			for left := startLeft; left <= endLeft; left++ {
				invalidSum += left * (base + 1)
			}
		}
	}
	return invalidSum
}
func part1(rangesNumbers []Range) int {
	invalidSum := 0
	for _, r := range rangesNumbers {
		start := r.Start
		startStr := strconv.Itoa(start)
		numLen := len(startStr)
		if numLen%2 != 0 {
			start = int(math.Pow10(numLen))
			numLen = len(startStr)
		}
		pow := numLen / 2

		left := start / int(math.Pow10(pow))
		joined := (left * int(math.Pow10(pow))) + left
		for joined <= r.End {
			if joined >= r.Start {
				invalidSum += joined
			}
			left++

			pow = len(strconv.Itoa(left))
			joined = (left * int(math.Pow10(pow))) + left
		}

	}
	return invalidSum
}

// % end

// % start
func part2(rangesNumbers []Range) int {
	invalidSum := 0
	for _, r := range rangesNumbers {
		startStr := strconv.Itoa(r.Start)
		endStr := strconv.Itoa(r.End)

		minLen := len(startStr)
		maxLen := len(endStr)

		var found []int

		for L := minLen; L <= maxLen; L++ {
			for k := 1; k < L; k++ {
				if L%k != 0 {
					continue
				}

				repeat := L / k
				multiplier := 0
				for i := range repeat {
					multiplier += int(math.Pow10(i * k))
				}

				minPattern := ceilDiv(r.Start, multiplier)
				maxPattern := int(math.Pow10(k)) - 1
				endPattern := r.End / multiplier
				if endPattern < maxPattern {
					maxPattern = endPattern
				}

				for pattern := minPattern; pattern <= maxPattern; pattern++ {

					val := pattern * multiplier
					if slices.Contains(found, val) {
						continue
					}
					if val >= r.Start && val <= r.End {
						invalidSum += val
						found = append(found, val)
					}
				}

			}

		}
	}
	return invalidSum
}

// % end

func main() {
	aoc.RunDay(os.Args, "inputs/day02.txt", parse, part1, part2)
}
