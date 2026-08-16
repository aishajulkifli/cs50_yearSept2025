#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 5000;

// Hash table
node *table[N];

// Number of words in dictionary
unsigned int word_count = 0;

// Hash function (djb2-like variant for better distribution)
unsigned int hash(const char *word)
{
    unsigned long hash_value = 5381;
    int c;
    while ((c = *word++))
    {
        hash_value = ((hash_value << 5) + hash_value) + tolower(c); // hash * 33 + c
    }
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    // Temporary buffer for reading words
    char temp[LENGTH + 1];

    // Read words one at a time
    while (fscanf(file, "%s", temp) != EOF)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, temp);

        // Hash word to obtain index
        unsigned int index = hash(temp);

        // Insert node into hash table (prepend)
        new_node->next = table[index];
        table[index] = new_node;

        word_count++;
    }

    fclose(file);
    return true;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Temporary lowercase copy of the word
    char temp[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        temp[i] = tolower(word[i]);
    }
    temp[len] = '\0';

    // Get hash index
    unsigned int index = hash(temp);

    // Traverse linked list at that index
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcmp(cursor->word, temp) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Returns number of words in dictionary if loaded, else 0
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        table[i] = NULL;
    }
    return true;
}
