#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);
}
