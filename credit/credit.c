#include <stdio.h>
#include <cs50.h>

int main(void)
{
   long card_number = get_long("Number: ");

   int last_digit = card_number % 10;

   printf("last_digit: %d\n", last_digit);

   card_number /= 10;

   printf("card_number: %ld\n", card_number);
}
