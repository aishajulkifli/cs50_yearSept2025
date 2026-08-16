import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):                 # Remove words that do not match the variable length

        for var in self.domains:

            for word in self.domains[var].copy():       # Create a copy because we'll be removing items

                if len(word) != var.length:             # Remove word if length doesn't match
                    self.domains[var].remove(word)

    def revise(self, x, y):             # Make x arc consistent with y

        revised = False

        overlap = self.crossword.overlaps[x, y]     # Get overlap information

        if overlap is None:                         # No overlap -> nothing to revise
            return False

        i, j = overlap

        for word_x in self.domains[x].copy():        # Check every word in x's domain

            match_found = False

            for word_y in self.domains[y]:            # Look for at least one matching word in y

                if word_x[i] == word_y[j]:
                    match_found = True
                    break

            if not match_found:                     # Remove word_x from x's domain
                self.domains[x].remove(word_x)
                revised = True

        return revised

    def ac3(self, arcs=None):                   # If arcs is None, initialize queue with all arcs in the problem; otherwise, use arcs as the initial queue

        if arcs is None:                        # Create initial queue with all arcs in the problem

            queue = []

            for x in self.crossword.variables:      # For each variable x, add arcs (x, y) for each neighbor y of x
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))

        else:
            queue = list(arcs)

        while queue:

            x, y = queue.pop(0)                 # Get an arc (x, y) from the queue

            if self.revise(x, y):


                if len(self.domains[x]) == 0:                               # Domain became empty
                    return False

                for neighbor in self.crossword.neighbors(x):                # Add neighboring arcs back

                    if neighbor != y:
                        queue.append((neighbor, x))

        return True

    def assignment_complete(self, assignment):          # Check whether all variables have assignment

        return len(assignment) == len(self.crossword.variables)     # All variables have assignment if the length of the assignment is equal to the number of variables in the crossword

    def consistent(self, assignment):           # Check if assignment satisfies all constraints

        used_words = set()          # Keep track of used words to check for duplicates

        for var in assignment:

            word = assignment[var]

            if len(word) != var.length:     # If the length of the assigned word does not match the variable's length, the assignment is inconsistent
                return False

            if word in used_words:          # If the word has already been used, the assignment is inconsistent
                return False

            used_words.add(word)

        for var1 in assignment:             # Check each pair of variables in the assignment to see if they overlap and if the overlapping letters match

            for var2 in assignment:

                if var1 == var2:            # If the two variables are the same, skip this pair
                    continue

                overlap = self.crossword.overlaps[var1, var2]       # Get the overlap information for the two variables

                if overlap is None:
                    continue

                i, j = overlap

                if assignment[var1][i] != assignment[var2][j]:     # If the overlapping letters do not match, the assignment is inconsistent
                    return False

        return True

    def order_domain_values(self, var, assignment):         # Return domain values ordered by least constraining value

        counts = []

        for value in self.domains[var]:                     # For each value in var's domain, count how many values it rules out for neighboring variables that are not yet assigned

            ruled_out = 0

            for neighbor in self.crossword.neighbors(var):  # For each neighbor of var that is not yet assigned, count how many values in the neighbor's domain are ruled out by value

                if neighbor in assignment:                  # If the neighbor is already assigned, skip it
                    continue

                overlap = self.crossword.overlaps[var, neighbor]        # Get the overlap information for var and the neighbor

                if overlap is None:
                    continue

                i, j = overlap

                for neighbor_word in self.domains[neighbor]:            # For each word in the neighbor's domain, check if it is ruled out by value

                    if value[i] != neighbor_word[j]:                    # If the overlapping letters do not match, neighbor_word is ruled out
                        ruled_out += 1

            counts.append((value, ruled_out))

        counts.sort(key=lambda item: item[1])                           # Sort values by the number of ruled out values, in ascending order

        return [value for value, count in counts]

    def select_unassigned_variable(self, assignment):                   # Return an unassigned variable not already part of assignment

        unassigned = []

        for var in self.crossword.variables:

            if var not in assignment:       # If var is already assigned, skip it

                domain_size = len(self.domains[var])

                degree = len(self.crossword.neighbors(var))

                unassigned.append((var, domain_size, degree))

        unassigned.sort(key=lambda item: (item[1], -item[2]))       # Sort unassigned variables by the size of their domain (in ascending order), and in case of a tie, by the number of neighbors they have (in descending order)

        return unassigned[0][0]     # [0][0] to return the variable from the sorted list of unassigned variables]

    def backtrack(self, assignment):    # Backtracking search algorithm to find a solution to the crossword CSP

        if self.assignment_complete(assignment):        # If the assignment is complete, return the assignment as a solution
            return assignment

        var = self.select_unassigned_variable(assignment)       # Select an unassigned variable using the select_unassigned_variable method

        for value in self.order_domain_values(var, assignment): # For each value in the variable's domain, ordered by least constraining value

            assignment[var] = value

            if self.consistent(assignment):         # If the assignment is consistent, recursively call backtrack with the new assignment

                result = self.backtrack(assignment)

                if result is not None:
                    return result

            del assignment[var]         # If the assignment is not consistent or if the recursive call did not find a solution, remove the assignment and try the next value

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

# python generate.py data/structure1.txt data/words1.txt
