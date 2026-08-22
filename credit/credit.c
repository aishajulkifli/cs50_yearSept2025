#include <stdio.h>
#include <cs50.h>

int main(void)
{
   long card_number = get_long("Number: ");

   int position = 1;

   while (card_number > 0)
      {
         int digit = card_number % 10;
         printf("digit: %d\n", digit);

         if (position % 2 == 0)
         {
            digit = digit * 2;
            if (digit > 9)
            {
               digit = digit - 9;
            }
            printf("digit * 2: %d\n", digit);
         }
         card_number /= 10;

         position = position + 1;
      }

      return 0;
}
