package adventofcode2025

import (
	"os"
	"path/filepath"
)

/*
Helper func to adjust input path for debugging and running from console
*/
func FindInputFile(filename string) string {
	if _, err := os.Stat(filename); err == nil {
		return filename
	}
	altFilePath := filepath.Join("..", "..", filename)
	if _, err := os.Stat(altFilePath); err == nil {
		return altFilePath
	}
	return filename
}
