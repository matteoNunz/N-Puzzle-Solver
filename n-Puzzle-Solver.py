"""
Author: Matteo Nunziante
Date: 27/09/2021

Algorithm: A*

OpenList -> contains all the nodes that are being generated
ClosedList -> contains each node explored after it's neighboring nodes are discovered

Optimization -> new node already present in the closedList or in the openList won't be put in the openList

Calculate the "distance" from the goal:
    f-score = h-score + g-score

    h-score (positional) = number of misplaced tiles between the current state and the goal state
    h-score (proportional) = calculate the difference in module between position of numbers in the current node
                                and the positions in the final configuration
    g-score = number of nodes traversed from the start node to get to the
                current node

Input-> specified the size of the puzzle
        specified the start configuration as follow
        1 2 3
        4 5 6
        7 8 _
"""


class Node:
    def __init__(self, data, level, fVal):
        """
        Initialize the node
        :param data: is the puzzle
        :param level: level of the node
        :param fVal: the f value
        """
        self.data = data
        self.level = level
        self.fVal = fVal

    def generateChild(self):
        """
        Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right}
        """
        x, y = self.find(self.data, '_')  # take the coordinate of the '_' character
        """
        valList contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively
        """
        valList = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []

        # For every element in valList generate the child
        for val in valList:
            child = self.shuffle(self.data, x, y, val[0], val[1])  # Matrix , x , y , newX , newY
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
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
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            tempPuz = []
            tempPuz = self.copy(puz)
            temp = tempPuz[x2][y2]
            tempPuz[x2][y2] = tempPuz[x1][y1]
            tempPuz[x1][y1] = temp
            return tempPuz
        else:
            return None

    def copy(self, root):
        """
        Copy function to create a similar matrix of a given node
        :param root: the node to duplicate
        :return: the duplicate node
        """
        duplicatePuz = []
        # For each row
        for row in root:
            duplicateRow = []
            for i in row:
                duplicateRow.append(i)
            duplicatePuz.append(duplicateRow)
        return duplicatePuz

    def find(self, puz, x):
        """
        Method used to find the coordinates of a specific character
        :param puz: is the puzzle (the matrix)
        :param x: is the char to find in the matrix
        :return: return the coordinates x and y of x in puz
        """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, size):
        """
        Initialize the puzzle size by the specified size,open and closed lists to empty
        :param size: is the size of the puzzle
        """
        self.size = size
        # Initialize the list as empty
        self.openList = []
        self.closedList = []

    def accept(self):
        """
        Accept the puzzle from the user
        :return: the puzzle
        """
        puz = []
        for i in range(0, self.size):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal):
        """
        Heuristic Function to calculate heuristic value f(x) = h(x) + g(x)
        :param start: h(x)
        :param goal: g(x)
        :return: return the f value
        """
        return self.hProportional(start.data, goal) + start.level

    def hPosition(self, start, goal):
        """
        Calculate the difference between the current puzzle and the final one -> check just if a number is in the right position
        :param start: the current node
        :param goal: the final configuration
        :return: return the h value
        """
        temp = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def hProportional(self, start, goal):
        """
        Calculate the difference between the current puzzle and the final one -> average position
        :param start:  the current node
        :param goal: the final configuration
        :return: return the h value
        """
        value = 0
        # Create the node corresponding to the final configuration
        goalNode = Node(goal, 0, 0)
        for i in range(0, self.size):
            for j in range(0, self.size):
                # Take the coordinate if the number start[i][j] in the goal configuration
                x, y = goalNode.find(goal, start[i][j])
                # Calculate the sqrt of the distance between the numbers
                value += K * (((abs(x - i) ** 2 + abs(y - j) ** 2)) ** (1 / 2))
        return value

    def process(self):
        """
        Accept Start and Goal Puzzle state
        """
        print("Enter the start state matrix \n")
        start = self.accept()
        # print("Enter the goal state matrix \n")
        # goal = self.accept()
        # goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '_']]

        # Generate the goal matrix
        goal = []
        for i in range(0 , self.size):
            goalRow = []
            for j in range(0 , self.size):
                if i == self.size - 1 and j == self.size - 1:
                    goalRow.append('_')
                else:
                    goalRow.append(str(i * self.size + j + 1))
            goal.append(goalRow)

        # Create the node
        start = Node(start, 0, 0)
        start.fVal = self.f(start, goal)

        # Put the start node in the open list
        self.openList.append(start)
        print("\n\n")

        while True:
            # Take the current node
            cur = self.openList[0]

            # Print the arrow
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for row in cur.data:
                for i in row:
                    print(i, end=" ")
                print("")

            """
            If the difference between current and goal node is 0 we have reached the goal node
            Position method for h is more efficient in that case
            """
            if self.hPosition(cur.data, goal) == 0:
                break

            for node in cur.generateChild():
                node.fVal = self.f(node, goal)
                self.addNode(node)
            self.closedList.append(cur)
            del self.openList[0]

            """
            Sort the open list based on the f value
            """
            self.openList.sort(key=lambda x: x.fVal, reverse=False)

    def addNode(self, node):
        """
        Add a node if it isn't already in the openList and in the closedList
        :param node: is the new node to add
        """
        for nodeInList in self.openList:
            # If the configuration is already present return
            if nodeInList.data == node.data:
                return

        for nodeInList in self.closedList:
            # If the configuration is already present return
            if nodeInList.data == node.data:
                return

        # If the configuration is not present add the node to the list
        self.openList.append(node)
        return


# K is necessary with size > 3 -> to increase the gap in the calculus of hProportional(x)
K = 1000

# Start the game
if __name__ == '__main__':

    # Ask the size to the user
    size = 0
    while True:
        print("Insert the size of the matrix")
        try:
            size = int(input())
            break
        except:
            print("Bad format")
    puz = Puzzle(size)

    # Start the computation
    puz.process()

    print("Element in the closed list are: " + str(len(puz.closedList)))
    print("Element in the open list are:   " + str(len(puz.openList)))
    print("The depth is:   " + str(puz.openList[0].level))
