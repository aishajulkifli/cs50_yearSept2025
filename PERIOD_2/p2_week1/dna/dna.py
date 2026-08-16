import csv      # import csv to read the database CSV file and store it in a list of dictionaries
import sys      # import sys to access command-line arguments and exit the program if necessary


def main():
    if len(sys.argv) != 3:                          # promt correct command
        sys.exit("Usage: python dna.py databases/small.csv sequences/1.txt")

    with open(sys.argv[1], "r") as database_file:    # sys system argument 1 is the database CSV file, open it for reading
        reader = csv.DictReader(database_file)       # Read the database CSV file
        database = [row for row in reader]           # store all rows in a list of dictionaries

    with open(sys.argv[2], "r") as sequence_file:   # Read the DNA sequence file
        sequence = sequence_file.read()             # read full DNA string

    str_counts = {}                                 # Count STRs (Short Tandem Repeats)

    for key in database[0].keys():                  # go through column names
        if key == "name":
            continue
        str_counts[key] = longest_match(sequence, key)

    for row in database:
        match = True                                # Compare STR counts with each person in the database
        for key in row.keys():
            if key == "name":
                continue

            if int(row[key]) != str_counts[key]:
                match = False
                break

        if match:
            print(row["name"])                       # print name if match found
            return

    print("No match")                                # If no match found

def longest_match(sequence, subsequence):
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run

main()
