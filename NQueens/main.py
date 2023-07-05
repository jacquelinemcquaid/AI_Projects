import copy
import sys
import time
import numpy
import numpy as np
import random

#N Queens Problem
#No two queens are in the same row or same diagonal

#Idea: Have helper functions that find the best overall next move (the next move that will lead to the least constraints)
#Use hill climbing as a local search method: store the current best state, and only change it if it improves

#Function to solve the n queens problem
def nQueens(n):

    #Goal: put n queens on an nxn board

    #States: configurations of the 4 queens (in 4 columns)
    #Operators: Move queen in a column
    #Goal test: no attacks
    #Evaluation function: number of attacks

    #Creating nxn array
    #initialBoard = np.zeros(shape=(n, n))

    #An array will store the location of each queen
    #indices 0 to n-1 represent the i,j values of queens 1-n, respectfully
    location = []

    #Randomly place queens on the board
    #Randomly place each queen in each column
    for i in range(0, n):
        #Random number between 0 and n-1 to determine where in the column to randomly place each queen
        randomPlacement = random.randint(0, n-1)
        #initialBoard[randomPlacement][i] = i+1
        location.append([randomPlacement, i])

    #Find the best queen to move and the best row index to move this queen that
    #results in the least constraints on the board
    bestQueen, minIndex = hillClimbing(location)

    #Keep calling the hill climbing local search method until the problem is solved
    #("COMPLETE" is reutrned from the hillClimbing function if there are 0 constraints on the board)
    while bestQueen != "COMPLETE":
        #If there is no better index after calling the hill climbing function, we have reached
        #A local optimum. Therefore, we can move the bestQueen returned to a random row
        #And continue calling the hillClimbing function until the global optimum is found
        if minIndex == "INCOMPLETE":
            location[bestQueen][0] = random.randint(0, len(location)-1)
        else:
            location[bestQueen][0] = minIndex

        #After changing the best queen to the best new row location, we call the hillClimbing function
        #again until the number of constraints are 0 on the board
        bestQueen, minIndex = hillClimbing(location)

    #Creating a new board to show the solution
    #solvedBoard = np.zeros(shape=(n, n))

    #Placing queens on the board
    #for i in range(0, len(location)):
        #solvedBoard[location[i][0]][i] = i+1

    # print("The initial board: ")
    # print(initialBoard)
    # print("The solved board: ")
    #print(solvedBoard)

    rowValuesOfQueens = []

    for i in range(0, len(location)):
        rowValuesOfQueens.append(location[i][0])

    return rowValuesOfQueens

#Takes as input the column index of the queen we want to move, and the location of all queens on the board
#Returns the best new row index and the total constraints on the board if we were to move the queen
def bestNewLocation(Q, location):

    #Declaring the min constraints and minIndex as the maximum integer value
    #to ensure the values are changed when checking the list of queen locations
    minConstraints = sys.maxsize
    minIndex = sys.maxsize

    #Creating a deep copy of the location array, where I can move values around
    #without affecting the current location of each queen
    copyArray = copy.deepcopy(location)

    #For each queen
    for i in range(0, len(location)):
        #If i isn't the current row index of the queen in column Q
        if i != location[Q][0]:
            #Changing the queen location and determining the total constraints if the queeen is moved to row i
            copyArray[Q][0] = i
            constraints = totalConstraints(copyArray)
            #If the number of constraints is less than the current minimum, than this location is better to
            #move the queen than the current minimum value
            if (constraints < minConstraints):
                minConstraints = constraints
                minIndex = i

    #Returning the best row index to move the queen, and the number of constraints on the board if the queen is
    #moved to this row
    return minIndex, minConstraints

#Takes as input a list of locations, where each column from 1-n represents queens 1-n respectively
#Returns the total number of constraints on the board
def totalConstraints(locations):

    #Keeping track of the total number of constraints
    constraintCount = 0

    #Iterating from the first column
    for i in range(0, len(locations)):
        #We only need to consider a constraint once, therefore compare to the columns greater than column i
        for j in range(i+1, len(locations)):
            # Checking if the queens are in the same row (using pseudocode from the lectures)
            if locations[i][0] == locations[j][0]:
                constraintCount += 1
            # Checking if the queens are in the same diagonal (using pseudocode from the lectures)
            if abs(locations[i][0] - locations[j][0]) == abs(i - j):
                    constraintCount += 1

    #Returning the total number of constraints on the board
    return constraintCount

#Takes as input the initial configuration of the board (an array with the location of each queen)
#Returns the best queen to move and the best row index to move it to, if it is better than the current state
#If there are no constraints on the board, it returns "COMPLETE"
#If we are at a local optimum, it returns "INCOMPLETE", and a random queen to change
def hillClimbing(initialConfiguration):

    #Calculating the total constraints on the current board
    totalCurrentConstraints = totalConstraints(initialConfiguration)

    #Array holding a tuple: (best index if we were to change this queen, number of constraints of this new configuration)
    numberOfConstraintsBestNewLocation = []

    #Iterating through each queen location in the initial configuration
    for queen in range(0, len(initialConfiguration)):
        #Finding the best row index and number of constraints if we were to move this queen to this new location
        bestIndex, constraints = bestNewLocation(queen, initialConfiguration)
        #Storing these values to later determined the best next move
        numberOfConstraintsBestNewLocation.append((bestIndex, constraints))

    #Declaring the bestQueen, the best new row index to move the queen, and the minimum constraints
    #of the board if we were to move this queen to the new location. Initializing these values as the
    #best values of moving the first queen in the initial configuration
    bestQueen = 0
    bestNewIndex = numberOfConstraintsBestNewLocation[0][0]
    minConstraints = numberOfConstraintsBestNewLocation[0][1]

    #Finding the index that results in a next move with the minimum constraints violated
    #By considering the best next moves of each individual queen from the current configuration
    for i in range(0, len(numberOfConstraintsBestNewLocation)):
        if numberOfConstraintsBestNewLocation[i][1] < minConstraints:
            minConstraints = numberOfConstraintsBestNewLocation[i][1]
            bestQueen = i
            bestNewIndex = numberOfConstraintsBestNewLocation[i][0]

    #Checking if moving the next best queen results in less constraints than the current configuration
    if minConstraints < totalCurrentConstraints:
        #Returning the queen to move, and the row index to move it to
        return bestQueen, bestNewIndex

    #If the move isn't better and there are more than 0 constraints, we have reached a local optimum
    elif totalCurrentConstraints > 0:
        return random.randint(0, len(initialConfiguration)-1), "INCOMPLETE"

    #If there are no better moves and the total current score is 0, the problem is complete
    else:
        return "COMPLETE", "COMPLETE"


print("Solving nxn Queens...")
locationOfQueens = nQueens(8)
print(locationOfQueens)







