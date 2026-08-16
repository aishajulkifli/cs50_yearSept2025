#include "helpers.h"
#include<math.h>

void grayscale(int height, int width, RGBTRIPLE image[height][width])           // Convert image to grayscale (./filter -g images/yard.bmp grayscale.bmp)
{
    //calculate the average picture value
    //set each color value to the average value

    float avg;
    for (int i = 0; i < height; i++)    // loop through each row
    {
        for (int j = 0; j < width; j++)
        {
            //calculate the average picture value
            avg = ((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)/3);     //Take the red, green, blue values of a pixel
            // set each color value to the average value
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }

    return;
}

void sepia(int height, int width, RGBTRIPLE image[height][width])             // Convert image to sepia (./filter -s images/stadium.bmp sepia.bmp)
{
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculate each each new color value using the sepia formula
            sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;

            //If a color goes above 255 → set it to 255 (RGB max).
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            // If a color goes above 255 → set it to 255 (RGB max).
            image[i][j].rgbtRed = sepiaRed > 255 ? 255 : sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen > 255 ? 255 : sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue > 255 ? 255 : sepiaBlue;
        }
    }
    return;
}

void reflect(int height, int width, RGBTRIPLE image[height][width])         // Reflect image (./filter -r images/courtyard.bmp reflect.bmp)
{
    for (int i = 0; i < height; i++)                                        // For each row
    {
        for (int j = 0; j < width / 2; j++)                                 // Only loop halfway across the row
        {
            RGBTRIPLE temp = image[i][j];                                   // Swap pixel at j with pixel at (width - 1 - j)
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

void blur(int height, int width, RGBTRIPLE image[height][width])           // Blur image
{
    RGBTRIPLE copy[height][width];                                         // Make a copy of the original image
    for (int i = 0; i < height; i++)                                       // Loop through every row
    {
        for (int j = 0; j < width; j++)                                    // Loop through every column
        {
            copy[i][j] = image[i][j];                                      // Copy pixel color to 'copy'
        }
    }

    for (int i = 0; i < height; i++)                                       // Compute the average of the 3x3 grid
    {
        for (int j = 0; j < width; j++)
        {
            int totalRed = 0;                                              // Sum of red values in the 3x3 grid
            int totalGreen = 0;                                            // Sum of green values in the 3x3 grid
            int totalBlue = 0;                                             // Sum of blue values in the 3x3 grid
            int count = 0;                                                 // How many valid pixels we've added

            for (int di = -1; di <= 1; di++)                               // Loop through the pixel’s neighbors (rows above, current, below)
            {
                for (int dj = -1; dj <= 1; dj++)                           // columns left, current, right
                {
                    int ni = i + di;                                       // neighbor row
                    int nj = j + dj;                                       // neighbor column

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)   // Step 4: Check boundaries (avoid going outside image)
                    {
                        totalRed += copy[ni][nj].rgbtRed;                  // Add neighbor’s red value
                        totalGreen += copy[ni][nj].rgbtGreen;              // Add neighbor’s green value
                        totalBlue += copy[ni][nj].rgbtBlue;                // Add neighbor’s blue value
                        count++;                                           // Count how many pixels were added
                    }
                }
            }

            // Step 5: Set the new pixel value in the original image
            image[i][j].rgbtRed = round((float) totalRed / count);
            image[i][j].rgbtGreen = round((float) totalGreen / count);
            image[i][j].rgbtBlue = round((float) totalBlue / count);
        }
    }
}
