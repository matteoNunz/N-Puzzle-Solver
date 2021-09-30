"""
Author: Matteo Nunziante
Date: 29/09/2021

Generator of N-puzzle starting configuration

Input: -size of the puzzle
       -number of random action to do on the puzzle
"""
from random import seed
from random import randint


def shufflePuzzle(puzzle , numberOfMoves):
    """
    Method that compute a certain amount of actions on the puzzle to create a random configuration
    :param puzzle: is the puzzle to shuffle
    :param numberOfMoves: is the number of move to do
    """
    seed()
    i = 0
    while i < numberOfMoves:
        # Find the coordinates of '_'
        x , y = find(puzzle , '_')
        """
        valList contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively
        """
        valList = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        # Make the random shuffle
        value = randint(0 , 3)
        result = shuffle(puzzle , x , y , valList[value][0] , valList[value][1])

        # If the action wasn't valid
        if result is None and i != 0:
            i -= 1

        i += 1


def shuffle(puz, x1, y1, x2, y2):
    """
    Move the blank space in the given direction and if the position value are out
        of limits the return None
    :param puz: is the current puzzle
    :param x1: x coordinate of '_'
    :param y1: y coordinate of '_'
    :param x2: new x coordinate of '_'
    :param y2: new y coordinate of '_'
    :return: the new puzzle or None if the value exceeded the limits
    """
    if x2 >= 0 and x2 < len(puz) and y2 >= 0 and y2 < len(puz):
        temp = puz[x2][y2]
        puz[x2][y2] = puz[x1][y1]
        puz[x1][y1] = temp
        return puz
    else:
        return None


def find(puz, x):
    """
    Method used to find the coordinates of a specific character
    :param puz: is the puzzle (the matrix)
    :param x: is the char to find in the matrix
    :return: return the coordinates x and y of x in puz
    """
    for i in range(0, len(puz)):
        for j in range(0, len(puz)):
            if puz[i][j] == x:
                return i, j


def generateStart(size):
    """
    Method used to generate the start state automatically
    :return: the puzzle
    """
    puzzle = []
    for i in range(0 , size):
        puzzleRow = []
        for j in range(0 , size):
            if i == size - 1 and j == size - 1:
                puzzleRow.append('_')
            else:
                puzzleRow.append(str(i * size + j + 1))
        puzzle.append(puzzleRow)
    return puzzle


def startGeneration():
    # Ask the size to the user
    size = 0
    while True:
        print("Insert the size of the puzzle")
        try:
            size = int(input())
            break
        except:
            print("Bad format")

    # Ask the number of actions to the user
    numberOfMoves = 0
    while True:
        print("Insert the number of random action to do on the puzzle")
        try:
            numberOfMoves = int(input())
            break
        except:
            print("Bad format")

    print("Starting the computation...")

    # Generate the starting state
    puzzle = generateStart(size)

    # Shuffle the puzzle
    shufflePuzzle(puzzle , numberOfMoves)

    print("Computation ended correctly!")

    # Print the puzzle
    for row in puzzle:
        for i in row:
            print(i, end=" ")
        print("")


if __name__ == "__main__":
    startGeneration()

