#include <cs50.h>   // For get_string()
#include <stdio.h>  // For printf()
#include <string.h> // For strlen()
#include <ctype.h>  // For character checks like isalpha()
#include <math.h>   // For round() function

// Function prototypes, declare the existence of these functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");         // Prompt for some text

    int letters = count_letters(text);          // Count the number of letters, words, and sentences
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float) letters / words * 100;         // letter per 100 words as Coleman–Liau formula
    float S = (float) sentences / words * 100;       // sentences per 100 words as Coleman–Liau formula
    float index = 0.0588 * L - 0.296 * S - 15.8;     // float index calculation to get more precise result
    int grade = round(index);                        // round the float index to nearest integer

    if (grade < 1)               // Print result below than 1
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)       // Print result 16 or above
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);    // Print result between 1 and 15
    }
}

    int count_letters(string text)      // letters count variable
{
    int count = 0;        // Initialize count to 0
    for (int i = 0, n = strlen(text); i < n; i++)   //  Loop through each character in the text
    {
        if (isalpha(text[i]))
        {
            count++;        // Increment count if character is a letter
        }
    }
    return count;
}

    int count_words(string text)    // words count variable
{
    int count = 1;          // start at 1 because last word doesn’t end with a space
    for (int i = 0, n = strlen(text); i < n; i++)   // Loop through each words in the text
    {
        if (text[i] == ' ') // Increment count when a space is found
        {
            count++;        // Each space indicates a new word
        }
    }
    return count;
}

    int count_sentences(string text)    // sentences count variable
{
    int count = 0;        // Initialize count to 0
    for (int i = 0, n = strlen(text); i < n; i++)   // Loop through each character in the text
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?') // Check for sentence-ending punctuation
        {
            count++;        // Increment count for each sentence found
        }
    }
    return count;
}
