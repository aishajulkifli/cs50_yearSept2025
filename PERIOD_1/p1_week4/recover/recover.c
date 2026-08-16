#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>                         // for uint8_t (8-bit unsigned integer)

#define BLOCK_SIZE 512                      // Define the size of each data block (512 bytes per block)

int main(int argc, char *argv[])
{
    if (argc != 2)                          // run program with 2 arguments ( ./recover card.raw)
    {
        printf("Usage: ./recover FILE\n");
        return 1;                           // Return error if the number of arguments is not 2
    }

    FILE *card = fopen(argv[1], "r");       // Open file in read mode
    if (card == NULL)                       // Check if file cannot be opened
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];             // Temporary storage for 512-byte blocks
    FILE *img = NULL;                       // Pointer to the JPEG file we’ll write to
    int jpeg_count = 0;                     // Counter to name files (000.jpg, 001.jpg…)
    char filename[8];                       // To store the file name (e.g. "000.jpg" + '\0')

    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)    // fread returns the number of bytes read. While 512 bytes are read, continue
    {
        if (buffer[0] == 0xff &&            // 1st byte of JPEG
            buffer[1] == 0xd8 &&            // 2nd byte of JPEG
            buffer[2] == 0xff &&            // 3rd byte of JPEG
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)                                      // Checks if a previous JPEG file is open
            {
                fclose(img);                                      // close old file
            }

            sprintf(filename, "%03i.jpg", jpeg_count);            // Create a new filename (e.g. "000.jpg")

            img = fopen(filename, "w");                           // Open new file for writing

            jpeg_count++;                                         // Move to the next JPEG count
        }

        if (img != NULL)                                          // write the current 512-byte block
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);                   // rebuilds the JPEG piece by piece
        }
    }

    if (img != NULL)                                              // check if an image is open
    {
        fclose(img);                                              // close image properly
    }

    fclose(card);                                                 // Close the memory card file

    return 0;                                                     // operating system ran successfully
}

// run the program (./recover card.raw)
// to delet the jpg (rm -f *.jpg) (rm = remove) (-f = force delet) (* = asterisk / any characters, of any length)
