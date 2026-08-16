#include <cs50.h>       // get_int function
#include <stdio.h>      // printf function

int main(void)
{
    int height;         // variable to store pyramid height

    // prompt for height
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0);        // ensure height is positive

    // build pyramid
    for (int i = 1; i <= height; i++)       // i is input height, loop control the row
    {
        // print spaces
        for (int j = 0; j < height - i; j++)    // if height is 4, first row prints 3 spaces
        {
            printf(" ");
        }

        // print hashes
        for (int j = 0; j < i; j++)    // if height is 4, first row prints 1 hash
        {
            printf("#");
        }

        printf("\n");       // move to next line after each row
    }
}
