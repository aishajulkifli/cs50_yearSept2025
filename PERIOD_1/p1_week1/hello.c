#include <cs50.h>       // get_string function
#include <stdio.h>      // printf function

int main(void)
{
    string firstname = get_string("What's your name? ");    // prompt for user name
    printf("hello, %s\n", firstname);                       // greet the user
}

