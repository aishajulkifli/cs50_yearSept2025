/*
    Plurality is for voting
    W simplest election system
    Majority is the winner
*/

#include <cs50.h>               // string library from cs50
#include <stdio.h>              // printf library
#include <string.h>             // strcmp library - string compare

#define MAX 9                   // Max number of candidates

typedef struct                  // Candidates have name and vote count
{
    string name;
    int votes;
} candidate;

candidate candidates[MAX];      // Array of candidates

int candidate_count;            // Number of candidates

bool vote(string name);         // Function prototypes
void print_winner(void);

int main(int argc, string argv[])
{
    if (argc < 2)                   // Check for invalid usage(cannot be less than 2)
    {
        printf("Usage: plurality [candidate ...]\n");           //error message
        return 1;
    }

    candidate_count = argc - 1;      // Populate array of candidates(not more than MAX)
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);    // error message
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)                   // candidates array
    {
        candidates[i].name = argv[i + 1];                       // user's input w candidates names
        candidates[i].votes = 0;                                // votes starts w 0
    }

    int voter_count = get_int("Number of voters: ");            // prompt user for voters amount

    for (int i = 0; i < voter_count; i++)                       // Loop over all voters
    {
        string name = get_string("Vote: ");                     // prompt for candidates name to vote

        if (!vote(name))                                        // Check for invalid vote
        {
            printf("Invalid vote.\n");                          // error message
        }
    }

    print_winner();                                             // Display winner of election
}

bool vote(string name)                                          // Update vote totals given a new vote
{
    for (int i = 0, n = candidate_count; i < n; i++)            // loop through all candidates to find the match
    {
        if(strcmp(candidates[i].name, name) == 0)               // strcmp(string compare to return 0 if match)
        {
            candidates[i].votes++;
            return true;                                        // found the match
        }
    }
    return false;                                               // if no match found
}

void print_winner(void)                                         // Find and print the winner of the most votes
{
    int highest = 0;                                            // refer to the bool functions for the match
    for (int i = 0, n = candidate_count; i < n; i++)            // find the highest votes received
    {
        if(candidates[i].votes > highest)
        {
            highest = candidates[i].votes;                      // the updated highest votes
        }
    }

    for (int i = 0, n = candidate_count; i < n; i++)            // for the tie's votes received
    {
        if(candidates[i].votes == highest)
        {
            printf("%s\n", candidates[i].name);                 // print the name
        }
    }
}
