#include <stdio.h>
#include <cs50.h>

void print_row(int spaces, int left_bricks, int gap, int right_bricks);

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        print_row(height - i - 1, i + 1, 2, i + 1);
    }

}

void print_row(int spaces, int left_bricks, int gap, int right_bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }

    for (int i = 0; i < left_bricks; i++)
    {
        printf("#");
    }

    for (int i = 0; i < gap; i++)
    {
        printf("  ");
    }

    for (int i = 0; i < right_bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}
