package main

// AoC solution template -- parts as pure functions; bench via `--bench` (BENCH-PLAN.md)
//
// % unsolved

import (
	aoc "advent-of-code-2025"
	"os"
	"strings"
)

type Parsed []string

func parse(data string) Parsed {
	// TODO: adjust based on input type
	return strings.Split(data, "\n")
}

// % start
func part1(p Parsed) int {
	// TODO: solve part 1
	_ = p
	return 0
}
// % end

// % start
func part2(p Parsed) int {
	// TODO: solve part 2
	_ = p
	return 0
}
// % end

func main() {
	aoc.RunDay(os.Args, "inputs/day{DAY2}.txt", parse, part1, part2)
}
