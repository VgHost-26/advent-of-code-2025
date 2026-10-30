package adventofcode2025

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

/*
Generic day runner (see BENCH-PLAN.md).

Normal mode:  day binary [--input inputs/dayNN.txt]

	prints "Solving with input from <path>" and one line per part.

Bench mode:   day binary --bench [--input PATH] [--runs N]

	parse() runs once untimed, each part gets one warmup + N timed runs
	(time.Since around the call only -- no startup/IO in the measurement),
	then prints exactly one JSON line:
	{"answers": {"1": "...", "2": "..."},
	 "timings": {"1": [<ms>...], "2": [<ms>...]}}

parse/part2 may be nil while a day is only partially solved; the solution
file itself carries the `% unsolved` marker until then.
*/
func RunDay[P any, A1 any, A2 any](args []string, defaultInput string,
	parse func(string) P, part1 func(P) A1, part2 func(P) A2) {

	benchMode := false
	inputFlag := defaultInput
	runs := 10

loop:
	for i := 1; i < len(args); i++ { // args[0] is the binary itself
		arg := args[i]
		switch {
		case arg == "--bench":
			benchMode = true
		case strings.HasPrefix(arg, "--input="):
			inputFlag = strings.TrimPrefix(arg, "--input=")
		case arg == "--input":
			if i+1 < len(args) {
				i++
				inputFlag = args[i]
			}
		case strings.HasPrefix(arg, "--runs="):
			runs, _ = strconv.Atoi(strings.TrimPrefix(arg, "--runs="))
		case arg == "--runs":
			if i+1 < len(args) {
				i++
				if n, err := strconv.Atoi(args[i]); err == nil {
					runs = n
				}
			}
		case strings.HasPrefix(arg, "-"):
			// ignore unknown flags
		default:
			inputFlag = arg // positional path (old convention)
		}

		if arg == "--" {
			break loop
		}
	}

	inputPath := FindInputFile(inputFlag)
	data, err := os.ReadFile(inputPath)
	if err != nil {
		panic(err)
	}
	parsed := parse(string(data))

	if !benchMode {
		fmt.Printf("Solving with input from %s\n", inputFlag)
		fmt.Printf("Part 1: %v\n", part1(parsed))
		if part2 != nil {
			fmt.Printf("Part 2: %v\n", part2(parsed))
		}
		return
	}

	answers := map[string]string{}
	timings := map[string][]float64{}

	run1 := func() any { return part1(parsed) }
	runs2 := []func() any{}
	if part2 != nil {
		runs2 = append(runs2, func() any { return part2(parsed) })
	}

	measure := func(label string, run func() any) {
		run() // untimed warmup
		ms := make([]float64, 0, runs)
		var answer any
		for i := 0; i < runs; i++ {
			start := time.Now()
			answer = run()
			ms = append(ms, float64(time.Since(start).Nanoseconds())/1e6)
		}
		answers[label] = fmt.Sprint(answer)
		timings[label] = ms
	}

	measure("1", run1)
	if len(runs2) > 0 {
		measure("2", runs2[0])
	}

	out, err := json.Marshal(struct {
		Answers map[string]string    `json:"answers"`
		Timings map[string][]float64 `json:"timings"`
	}{answers, timings})
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
