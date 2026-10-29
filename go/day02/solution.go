package main

import (
	aoc "advent-of-code-2025"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Range struct {
	Start int
	End   int
}
type RangeString struct {
	Start string
	End   string
}

func ceilDiv(a, b int) int {
	return (a + b - 1) / b
}

func main() {
	inputFile := "inputs/day02.txt"
	if len(os.Args) > 1 {
		inputFile = os.Args[1]
	}

	inputPath := aoc.FindInputFile(inputFile)
	data, err := os.ReadFile(inputPath)
	if err != nil {
		panic(err)
	}
	// data := "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

	fmt.Printf("Solving with input from %s\n", inputFile)

	dataPairs := strings.Split(string(data), ",")
	var rangesNumbers []Range

	for _, pair := range dataPairs {
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

	// % start
	// Part 1

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
	fmt.Println("part 1 solution:", invalidSum)

	// Part 2

	invalidSum = 0
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
	// % end

	fmt.Println("part 2 solution: ", invalidSum)

}
