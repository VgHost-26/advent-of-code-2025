package main

import (
	"fmt"
	"os"
)

func main() {
	inputFile := "input.txt"
	if len(os.Args) > 1 {
		inputFile = os.Args[1]
	}

	data, err := os.ReadFile(inputFile)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Solving with input from %s\n", inputFile)
	_ = data
	// Part 1
	
	// Part 2
}
