package main

import (
	"strconv"

	aoc "advent-of-code-2025"
	"math"
	"os"
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

type Parsed struct {
	Directions []rune
	Distances  []int
}

func parse(data string) Parsed {
	var directions []rune
	var distances []int

	for _, val := range strings.Split(data, "\n") {
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

	return Parsed{Directions: directions, Distances: distances}
}

// % start
func part1(p Parsed) int {
	dialPosition := 50
	pointedZeros := 0

	for i := 0; i < len(p.Directions); i++ {
		dir := p.Directions[i]
		dist := p.Distances[i]

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
	return pointedZeros
}

// % end

// % start
func part2(p Parsed) int {
	dialPosition := 50
	pointedZeros := 0

	for i := 0; i < len(p.Directions); i++ {
		dir := p.Directions[i]
		dist := p.Distances[i]

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
	return pointedZeros
}

// % end

func main() {
	aoc.RunDay(os.Args, "inputs/day01.txt", parse, part1, part2)
}
