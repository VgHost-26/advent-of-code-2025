#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {
    std::string inputFile = "input.txt";
    if (argc > 1) {
        inputFile = argv[1];
    }

    std::ifstream file(inputFile);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << inputFile << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(file, line)) {
        // Process line
    }

    std::cout << "Solving with input from " << inputFile << std::endl;

    return 0;
}
