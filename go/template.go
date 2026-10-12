package main

import (
	aoc "advent-of-code-2025"
	"fmt"
	"os"
)

func main() {
	inputFile := "inputs/day01.txt"
	if len(os.Args) > 1 {
		inputFile = os.Args[1]
	}

	inputPath := aoc.FindInputFile(inputFile)
	data, err := os.ReadFile(inputPath)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Solving with input from %s\n", inputFile)
	_ = data
	// Part 1

	// Part 2
}
