#include <cs50.h>   // allows use of get_string for user input
#include <stdio.h>  // allows use of printf for output
#include <ctype.h>  // provides functions like isupper(), islower()
#include <string.h> // provides strlen() to get length of strings

//points for each alphabets, its an array where index 0 corresponds to 'A', index 1 to 'B', and so on.
int POINTS[]= {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);         // Function prototype: declares the compute_score function

int main(void)
{
    // Prompt both players to enter their words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("player 2: ");

    // Calculate each word's Scrabble score using compute_score()
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Compare the scores and print the correct result
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!");
    }
}

// Function that calculates the Scrabble score of a word
int compute_score(string word)
{
    int score = 0;  // total score for the word

    // Loop through each character in the word
    for (int i = 0, len = strlen(word); i < len; i++)   // starting from index 0 to length of the word
    {
        // Check if the character is uppercase A–Z
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A']; // Convert uppercase letter to A–Z index (0–25) and add corresponding points
        }
        // Check if the character is lowercase a–z
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a']; // Convert lowercase letter to the same A–Z index (0–25) and add corresponding points
        }
        // Non-letter characters are ignored (worth 0 points)
    }

    // Return the total score for this word
    return score;
}
