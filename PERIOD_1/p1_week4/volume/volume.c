// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    uint8_t header[HEADER_SIZE];                        // Copy header from input file to output file
    fread(header, HEADER_SIZE, 1, input);               // Reads 44 bytes from the input file (header) and stores them in the array header. fread(file read)
    fwrite(header, HEADER_SIZE, 1, output);             // Writes that same 44 bytes into the output file

    // TODO: Read samples from input file and write updated data to output file

    // Close files
    fclose(input);
    fclose(output);
}
