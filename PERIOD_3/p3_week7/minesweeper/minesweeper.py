"""
Minesweeper AI Project

This project creates an AI that can play the Minesweeper game.

The AI does not just guess randomly. Instead, it uses logic to figure out
which cells are safe and which cells contain mines.

The AI keeps track of:
- moves it has already made
- cells that are safe
- cells that are mines
- logical sentences about the board

Each sentence represents a group of cells and how many of them are mines.

Using this knowledge, the AI:
1. Marks safe cells and mines
2. Updates its knowledge when new information is found
3. Uses logical inference to discover new information
4. Chooses safe moves when possible
5. Chooses random moves only when necessary

This allows the AI to play the game intelligently.
"""


import itertools        # for combinations
import random


class Minesweeper():     # class for the game itself
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):         # initialize the game with given dimensions and number of mines

        self.height = height        # set height for the game board
        self.width = width          # set width for the game board
        self.mines = set()          # set to store the locations of mines

        # Create empty board
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)       # append False to indicate no mine in this cell
            self.board.append(row)      # append the row to the board, append is used to add elements to the end of a list

        # Add mines randomly
        while len(self.mines) != mines:     # keep adding mines until we have the desired number of mines
            i = random.randrange(height)    # generate a random row index
            j = random.randrange(width)     # generate a random column index
            if not self.board[i][j]:        # if there is no mine at this location, add a mine
                self.mines.add((i, j))      # add the location of the mine to the set of mines
                self.board[i][j] = True     # mark the cell on the board as containing a mine

        self.mines_found = set()            # set to keep track of mines that have been found by the player

    def print(self):
        for i in range(self.height):        # print the top border of the board
            print("--" * self.width + "-")  # print the horizontal border for the board
            for j in range(self.width):     # iterate through each cell in the row
                if self.board[i][j]:
                    print("|X", end="")     # if there is a mine in the cell, print "X" to indicate a mine
                else:
                    print("| ", end="")     # if there is no mine, print a blank space, | is used to separate cells visually
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):                # check if the given cell contains a mine
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):           # count the number of mines in the neighboring cells

        count = 0                           # initialize count of nearby mines to 0

        for i in range(cell[0] - 1, cell[0] + 2):       # iterate through the rows around the cell, from one row above to one row below
            for j in range(cell[1] - 1, cell[1] + 2):   # iterate through the columns around the cell, from one column to the left to one column to the right

                if (i, j) == cell:          # skip the cell itself, we only want to count neighboring cells
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:    # check if the neighboring cell is within the bounds of the board
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        return self.mines_found == self.mines       # check if the player has found all the mines, if the set of mines found is equal to the set of all mines, then the player has won


class Sentence():
    """
    Logical statement about Minesweeper
    """

    def __init__(self, cells, count):       # initialize a sentence with a set of cells and a count of how many of those cells are mines
        self.cells = set(cells)             # store the cells as a set for easy manipulation, sets are unordered collections of unique elements
        self.count = count

    def __eq__(self, other):                # check if two sentences are equal by comparing their cells and counts
        return self.cells == other.cells and self.count == other.count

    def __str__(self):                      # return a string representation of the sentence, showing the cells and the count of mines
        return f"{self.cells} = {self.count}"

    def known_mines(self):                  # if the count of mines is equal to the number of cells, then all those cells must be mines
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):                  # if the count of mines is zero, then all those cells must be safe
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):              # if a cell is marked as a mine, remove it from the sentence and decrease the count of mines by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):              # if a cell is marked as safe, remove it from the sentence, the count of mines does not change because we are only marking a cell as safe, not identifying a mine
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():                      # class for the AI player that will use logical reasoning to play the game

    def __init__(self, height=8, width=8):  # initialize the AI with the dimensions of the game board, the AI will keep track of its knowledge about the game state

        self.height = height                # set height for the AI's understanding of the game board
        self.width = width                  # set width for the AI's understanding of the game board

        self.moves_made = set()             # set to keep track of moves that the AI has already made, this helps the AI avoid repeating moves and allows it to make informed decisions based on past actions
        self.mines = set()                  # set to keep track of cells that the AI has identified as containing mines, this is crucial for the AI to avoid making moves that would result in hitting a mine
        self.safes = set()                  # set to keep track of cells that the AI has identified as safe, this allows the AI to make moves with confidence, knowing that it won't hit a mine
        self.knowledge = []                 # list to keep track of sentences that represent the AI's knowledge about the game state, each sentence is a logical statement about a group of cells and how many of them are mines, this knowledge base allows the AI to make inferences and deduce new information about the game board

    def mark_mine(self, cell):             # AI identifies a cell as a mine, it adds that cell to the set of mines and updates all sentences in its knowledge base to reflect this new information, marking a cell as a mine means that the AI will avoid making moves on that cell in the future, and it will also use this information to update its understanding of the game board, potentially leading to new inferences about other cells
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):            # when the AI identifies a cell as safe, it adds that cell to the set of safes and updates all sentences in its knowledge base to reflect this new information, marking a cell as safe means that the AI can confidently make moves on that cell in the future, and it will also use this information to update its understanding of the game board, potentially leading to new inferences about other cells
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):   # when the AI makes a move and learns how many neighboring cells contain mines, it adds this information to its knowledge base, this process involves several steps:

        # 1. mark move made
        self.moves_made.add(cell)

        # 2. mark safe
        self.mark_safe(cell)

        # 3. get neighbors
        neighbors = set()

        for i in range(cell[0] - 1, cell[0] + 2):           # iterate through the rows around the cell, from one row above to one row below
            for j in range(cell[1] - 1, cell[1] + 2):       # -1 to +1 means we are looking at the 3x3 grid centered around the cell

                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:

                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes:
                        neighbors.add((i, j))

        # 4. add sentence
        new_sentence = Sentence(neighbors, count)           # create a new sentence based on the neighbors and the count of mines, this sentence represents the AI's knowledge about the neighboring cells of the cell it just revealed, it states that among the neighboring cells, there are 'count' number of mines, and the rest are safe, this information will be added to the AI's knowledge base and can be used for future inferences
        self.knowledge.append(new_sentence)

        # 5. update knowledge repeatedly
        changed = True
        while changed:
            changed = False

            safes = set()
            mines = set()

            # collect safes & mines
            for sentence in self.knowledge:             # iterate through all sentences in the knowledge base to collect any cells that are known to be safe or mines based on the current sentences, this step is crucial for the AI to update its understanding of the game board and make informed decisions about future moves
                safes |= sentence.known_safes()         # the |= operator is used to perform a union of sets, it adds all elements from the known safes of the sentence to the safes set
                mines |= sentence.known_mines()

            # mark safes
            for cell in safes:                          # iterate through the cells that are known to be safe and mark them as safe in the AI's knowledge base, this allows the AI to confidently make moves on these cells in the future, knowing that they do not contain mines
                if cell not in self.safes:
                    self.mark_safe(cell)
                    changed = True

            # mark mines
            for cell in mines:                          # iterate through the cells that are known to be mines and mark them as mines in the AI's knowledge base, this allows the AI to avoid making moves on these cells in the future, reducing the risk of hitting a mine and losing the game
                if cell not in self.mines:
                    self.mark_mine(cell)
                    changed = True

            # remove empty sentences
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            # infer new sentences
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:

                    if s1 == s2:
                        continue

                    if s1.cells.issubset(s2.cells):

                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count

                        new = Sentence(new_cells, new_count)

                        if len(new.cells) > 0 and new not in self.knowledge:
                            new_sentences.append(new)

            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

    def make_safe_move(self):               # the AI looks through its knowledge base to find any cells that it has identified as safe and has not yet made a move on, if it finds such a cell, it returns that cell as the next move, this allows the AI to make informed decisions based on its knowledge of the game board, rather than guessing randomly, if there are no known safe moves available, the method returns None, indicating that the AI may need to make a random move or that the game is over
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):             # if the AI cannot find any safe moves, it will make a random move, this method generates a list of all possible moves (cells) that have not yet been made and are not known to be mines, if there are no such moves available, it returns None, otherwise it randomly selects one of the available moves and returns it as the next move for the AI to make, this allows the AI to continue playing even when it does not have enough information to make a safe move, although it may be risky, it is sometimes necessary in order to progress in the game

        choices = []

        for i in range(self.height):
            for j in range(self.width):

                cell = (i, j)

                if cell not in self.moves_made and cell not in self.mines:      # iterate through all cells on the board and add those that have not been moved on and are not known to be mines to the list of choices for random moves, this ensures that the AI only considers valid moves that do not involve hitting a mine or repeating a move, which helps to increase the chances of winning the game even when making random moves
                    choices.append(cell)

        if not choices:
            return None

        return random.choice(choices)
