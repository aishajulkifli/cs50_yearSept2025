#include <stdio.h>
#include <cs50.h>

int main(void)
{
   long card_number = get_long("Number: ");

   while (card_number > 0)
      {
         int digit = card_number % 10;
         printf("digit: %d\n", digit);
         card_number /= 10;
      }

      return 0;
}
