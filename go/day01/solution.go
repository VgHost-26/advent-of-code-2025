package main

import (
	aoc "advent-of-code-2025"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"unicode/utf8"
)

func positiveMod(a int, b int) int {
	mod := a % b
	if mod < 0 {
		return b + mod
	}
	return mod
}

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

	strData := strings.Split(string(data), "\n")
	var directions []rune
	var distances []int

	for _, val := range strData {
		if val == "" {
			break
		}
		dir, _ := utf8.DecodeRuneInString(val[0:1])
		dist, err := strconv.Atoi(val[1:])
		if err != nil {
			panic(err)
		}
		directions = append(directions, dir)
		distances = append(distances, dist)
	}

	// Part 1

	dialPosition := 50
	pointedZeros := 0

	for i := 0; i < len(directions); i++ {
		dir := directions[i]
		dist := distances[i]

		switch dir {
		case 'R':
			dialPosition += dist
		case 'L':
			dialPosition -= dist
		}

		dialPosition := positiveMod(dialPosition, 100)

		if dialPosition == 0 {
			pointedZeros++
		}
	}
	fmt.Printf("Part 1: %d\n", pointedZeros)

	// Part 2

	dialPosition = 50
	pointedZeros = 0

	for i := 0; i < len(directions); i++ {
		dir := directions[i]
		dist := distances[i]

		revolutions := int(math.Floor(float64(dist) / 100))
		var remainder int
		if dist > 100 {
			remainder = int(math.Remainder(float64(dist), 100))
		} else {
			remainder = dist
		}

		pointedZeros += revolutions
		prevDialPosition := dialPosition

		switch dir {
		case 'R':
			dialPosition += remainder
		case 'L':
			dialPosition -= remainder
		}

		nextDialPosition := positiveMod(dialPosition, 100)

		dialPosition = nextDialPosition

		if dialPosition == 0 {
			pointedZeros++
		} else {

			switch dir {
			case 'R':
				if dialPosition < prevDialPosition && prevDialPosition != 0 {
					pointedZeros++
				}
			case 'L':
				if dialPosition > prevDialPosition && prevDialPosition != 0 {
					pointedZeros++
				}
			}
		}

	}

	fmt.Printf("Part 2: %d", pointedZeros)

}
