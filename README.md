# N-Puzzle-Solver

Author: Matteo Nunziante

Date: 29/09/2021

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
                
Input-> 
        
        specify the size of the puzzle

        specify the start configuration as follow
        1 2 3
        4 5 6
        7 8 _
        
# N-Puzzle-Generator

Use the generator to create random configurations of any size to testify the algorithm

Input ->
    
    specify the size of the puzzle
    
    specify the number of actions to perform on the puzzle to get the final random configuration
