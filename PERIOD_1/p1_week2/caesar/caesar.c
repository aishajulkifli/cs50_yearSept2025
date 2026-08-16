/*
    The simple and early way to hide & protect messages by chnaging it letters
    It changed based on what nmber we key, the letter will move based on given key/nmber
*/

#include <cs50.h>    // cs50 library, to use get_string function
#include <stdio.h>   // standard input output C library. w/o it, no disply o/put (print result)
#include <string.h>  // function w string, to loop user's input (text lenght)
#include <ctype.h>   // to test and convert chatachters
#include <stdlib.h>  // standard utility library(convert string - int(atoi)ASCII-American Standard Code for Information Interchange)

bool only_digits(string s);                  // only 2 values(true or false)(yes or no) for answer
char rotate(char c, int key);                // declares function, shift one character by caesar

int main(int argc, string argv[])           // argument count (argc-count every input characters) (argv-typed the actual words)
{
    if (argc != 2)                          // to make sure user type the correct key
    {
        printf("Usage: ./caesar key\n");    // print the message
        return 1;                           // an error
    }

    if (!only_digits(argv[1]))                  // Check if argument if it has digits
    {
        printf("Usage: ./caesar key\n");        // show the correct command
        return 1;                               // an error
    }

    int key = atoi(argv[1]);                                // Convert argument into int

    string plaintext = get_string("plaintext:  ");          // Prompt user for a text

    printf("ciphertext: ");                                 // Print ciphertext
    for (int i = 0, n = strlen(plaintext); i < n; i++)      // loop each character
    {
        printf("%c", rotate(plaintext[i], key));            // mix each character using the rotate() function and print it
    }
    printf("\n");

    return 0;                                               // program end
}

bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)              // Loop through each character in the string
    {
        if (!isdigit(s[i]))                                 // If any character is not a digit (0–9), return false
        {
            return false;                                   // not all are digits
        }
    }
    return true;                                            // all are digits
}

char rotate(char c, int key)
{
    if (isupper(c))                                         // chck if Uppercase (A-Z)
    {
        return ( (c - 'A' + key) % 26 ) + 'A';              // start counting the char A=0, B=1
    }
    else if (islower(c))                                    // chck if Lowwercase (a-z)
    {
        return ( (c - 'a' + key) % 26 ) + 'a';               // start counting the char a=0, b=1
    }
    else
    {
        return c;                                           // other than alphabets, it is unchange
    }
}
