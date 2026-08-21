#include <cs50.h>
#include <stdio.h>

int calculate_coins(int cents);

int main(void)
{
    int cents;

    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);
}

int calculate_coins(int cents)
{
    
}
