#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::string word = "hangman";
    std::string guessed(word.length(), '_');
    std::vector<char> tried;
    int lives = 6;

    std::cout << "Welcome to Hangman!\n";

    while (lives > 0 && guessed != word) {
        std::cout << "\nWord: " << guessed << "\n";
        std::cout << "Tried letters: ";
        for (char c : tried) std::cout << c << ' ';
        std::cout << "\nLives left: " << lives << "\n";
        std::cout << "Guess a letter: ";

        char guess;
        std::cin >> guess;
        guess = std::tolower(guess);

        if (std::find(tried.begin(), tried.end(), guess) != tried.end()) {
            std::cout << "You already tried '" << guess << "'.\n";
            continue;
        }

        tried.push_back(guess);

        bool found = false;
        for (size_t i = 0; i < word.length(); ++i) {
            if (word[i] == guess) {
                guessed[i] = guess;
                found = true;
            }
        }

        if (found) {
            std::cout << "Good guess!\n";
        } else {
            std::cout << "Wrong guess!\n";
            --lives;
        }
    }

    if (guessed == word) {
        std::cout << "\nCongratulations! You guessed the word: " << word << "\n";
    } else {
        std::cout << "\nGame over! The word was: " << word << "\n";
    }

    return 0;
} 