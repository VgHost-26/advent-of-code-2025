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

type Parsed [][]int

func parse(data string) Parsed {
	// TODO: adjust based on input type
	var banks [][]int
	dataSplitted := strings.Split(data, "\n")

	for _, dataLine := range dataSplitted {
		var batteries []int
		_batteries := strings.Split(dataLine, "")

		for _, _battery := range _batteries {
			bInt, err := strconv.Atoi(_battery)
			if err != nil {
				panic(err)
			}
			batteries = append(batteries, bInt)
		}
		banks = append(banks, batteries)
	}
	return banks
}

// % start
func part1(p Parsed) int {
	sum := 0
	for _, b := range p {
		bank := slices.Clone(b) // mutate prevention
		dec := slices.Max(bank[:len(bank)-1])
		index := slices.Index(bank, dec)

		bank = slices.Delete(bank, 0, index+1)
		unit := slices.Max(bank)

		power := dec*10 + unit
		sum += power
	}

	return sum
}

// % end

// % start
func part2(p Parsed) int {
	sum := 0
	for _, b := range p {
		bank := slices.Clone(b)
		totalPower := 0
		for batteriesLefft := 11; batteriesLefft >= 0; batteriesLefft-- {
			power := slices.Max(bank[:len(bank)-batteriesLefft])
			index := slices.Index(bank, power)
			totalPower += power * int(math.Pow10(batteriesLefft))
			bank = slices.Delete(bank, 0, index+1)
		}
		sum += totalPower
	}

	return sum
}

// % end

func main() {
	exampleInput := `987654321111111
811111111111119
234234234234278
818181911112111`

	parsedExample := parse(exampleInput)
	fmt.Println(part1(parsedExample))
	fmt.Println(part2(parsedExample))

	aoc.RunDay(os.Args, "inputs/day03.txt", parse, part1, part2)
}
