#include <cs50.h>                 // include cs50 library for get_int and get_string functions
#include <stdio.h>                // include standard input output library for printf function
#include <string.h>               // include string library for strcmp function - compare two strings

#define MAX_VOTERS 100                            // Max voters and candidates
#define MAX_CANDIDATES 9

int preferences[MAX_VOTERS][MAX_CANDIDATES];      // preferences[i][j] is jth preference for voter i

typedef struct                                    // define the structure of candidates
{
    string name;                                  // candidate's name
    int votes;                                    // candidate's votes
    bool eliminated;                              // check if the candidate has been elimated
} candidate;

candidate candidates[MAX_CANDIDATES];             // Array of candidates

int voter_count;                                  // amount of the voters
int candidate_count;                              // amount of the candidates

bool vote(int voter, int rank, string name);      // Function prototypes(Records a single voter’s ranked preference)
void tabulate(void);                              // Counts votes for the current round of the election
bool print_winner(void);                          // Check if any candidates won the election
int find_min(void);                               // Find the MIN votes to be eliminated
bool is_tie(int min);                             // To check if there's any tie candidates
void eliminate(int min);                          // To eliminate the lowest votes

int main(int argc, string argv[])
{
    if (argc < 2)                                   // Check for invalid usage(not less than 2)
    {
        printf("Usage: runoff [candidate ...]\n");  // error message
        return 1;
    }

    candidate_count = argc - 1;                     // number of candidates (not more than the MAX)
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);     // error message
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)       // candidates array
    {
        candidates[i].name = argv[i + 1];           // candidate's name
        candidates[i].votes = 0;                    // the votes starts w 0
        candidates[i].eliminated = false;           // no eliminated yet
    }

    voter_count = get_int("Number of voters: ");    // prompt for the amounts of voter
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);             // error message
        return 3;
    }

    for (int i = 0; i < voter_count; i++)                       // Keep querying for votes
    {

        for (int j = 0; j < candidate_count; j++)               // Query for each rank (1st, 2nd, 3rd ...)
        {
            string name = get_string("Rank %i: ", j + 1);       // prompt for candidates' name

            if (!vote(i, j, name))                              // Record vote, unless it's invalid (Stop the entire program and exit with error code 4)
            {
                printf("Invalid vote.\n");                      // error message
                return 4;
            }
        }

        printf("\n");
    }

    while (true)                                                // Keep holding runoffs until winner exists
    {
        tabulate();                                             // Calculate votes for non emilated candidates

        bool won = print_winner();                              // Check if there's a winner
        if (won)
        {
            break;
        }

        int min = find_min();                                   // Find the remaining MIN votes candidates
        bool tie = is_tie(min);                                 // Find if any tie votes

        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        eliminate(min);                                           // Eliminate anyone with minimum number of votes

        for (int i = 0; i < candidate_count; i++)                 // Reset vote counts back to zero
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

bool vote(int voter, int rank, string name)             // Record preference if vote is valid
{
    for (int i = 0; i < candidate_count; i++)           // Loop through all candidates
    {
        if (strcmp(candidates[i].name, name) == 0)      // If the name matches the candidate
        {
            preferences[voter][rank] = i;               // Store the candidate index in preferences
            return true;
        }
    }

    return false;                                        // Name not found among candidates
}

void tabulate(void)                                      // Tabulate votes for non-eliminated candidates(counts votes for each round of the runoff)
{
    for (int i = 0; i < voter_count; i++)                // Loop over all voters
    {
        for (int j = 0; j < candidate_count; j++)        // For each voter, go through their ranked preferences
        {
            int candidate_index = preferences[i][j];     // Get the candidate index (their jth preference)

            if (!candidates[candidate_index].eliminated) // Check if this candidate is still in the running (not eliminated)
            {
                candidates[candidate_index].votes++;     // Add one vote to this candidate

                break;
            }
        }
    }
}

bool print_winner(void)                                 // Print the winner of the election, if there is one
{
    int majority = voter_count / 2;                     // A majority is more than half of total voters

    for (int i = 0; i < candidate_count; i++)           // Check each candidate’s vote count
    {
        if (!candidates[i].eliminated && candidates[i].votes > majority)      // Only consider candidates still in the race (&&=AND(check two conditions at once))
        {
            printf("%s\n", candidates[i].name);         // Print the winner’s name
            return true;                                // Election won
        }
    }

    return false;                                        // If no candidate has more than half, election continues
}

int find_min(void)                                      // Return the minimum number of votes any remaining candidate has
{
    int min = 999999;                                   // start with a large number (variable) for easy calculate

    for (int i = 0; i < candidate_count; i++)           // Loop through all candidates
    {
        if (!candidates[i].eliminated && candidates[i].votes < min)         // Check only candidates who are still in the race (not eliminated)
        {
            min = candidates[i].votes;                  // update min to this smaller vote count
        }
    }

    return min;                                         // return the smallest number of votes found
}

bool is_tie(int min)                                    // Return true if the election is tied between all candidates, false otherwise
{
    for (int i = 0; i < candidate_count; i++)           // Loop through all candidates
    {
        if (!candidates[i].eliminated && candidates[i].votes != min)         // If a candidate is still in the race and has votes *different* from the minimum,
        {
            return false;
        }
    }

    return true;                                         // If we loop through everyone and find no differences, candidates have the same number of votes
}

void eliminate(int min)                                 // Eliminate the candidate (or candidates) in last place
{
    for (int i = 0; i < candidate_count; i++)           // Loop through all candidates
    {
        if (!candidates[i].eliminated && candidates[i].votes == min)        // If candidate is still in the race AND has the minimum number of votes, eliminate them
        {
            candidates[i].eliminated = true;            // mark candidate as eliminated
        }
    }
}
