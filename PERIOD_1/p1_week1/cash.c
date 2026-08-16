#include <cs50.h>       // For get_int
#include <stdio.h>      // For printf

// Function prototypes for coin calculations
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    int cents;          // Variable to store change owed
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);  // Ensure non-negative input

    // Calculate number of coins
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;      // how many quarters fit

    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;         // remaining how many dimes fit

    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;        // remaining how many nickels fit

    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;        // remaining how many pennies fit until 0

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print result
    printf("%i\n", coins);              // % placeholder for an integer
}

// Function definitions
int calculate_quarters(int cents)       // each function takes the amount left in cents and divides it by the coin value
{
    return cents / 25;
}

int calculate_dimes(int cents)
{
    return cents / 10;
}

int calculate_nickels(int cents)
{
    return cents / 5;
}

int calculate_pennies(int cents)
{
    return cents / 1;
}
