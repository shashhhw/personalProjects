# %% Import necessary libraries
import numpy as np
import random

# %% Define necessary functions
def chooseSign():
    
    userSign = input("Do you want to be 'X' or 'O'?").upper()

    if userSign == 'X':

        compSign = 'O'
        print("User Sign: %c and Computer Sign: %c" %(userSign, compSign))
        return userSign, compSign

    elif userSign == 'O':

        compSign = 'X'
        print("User Sign: %c and Computer Sign: %c" %(userSign, compSign))
        return userSign, compSign

    else:

        print("You chose %c! Wrong input, choose again!" %userSign)
        return chooseSign()

def makeGrid():

    initialGridMatrix = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    initialGridMatrix = np.array(initialGridMatrix)
    
    return initialGridMatrix

def showGridMatrix(gridMatrix):

    for row in range(np.shape(gridMatrix)[0]):
        print(gridMatrix[row, 0], end='')
        print(" |", end='')
        print(gridMatrix[row, 1], end='')
        print(" |", end='')
        print(gridMatrix[row, 2])

        if row != 2:
            print("_ _ _ _ _")
    
    print("\n")

def returnCoordinates(input):

    coord = {
        '1': [0, 0],
        '2': [0, 1],
        '3': [0, 2],
        '4': [1, 0],
        '5': [1, 1],
        '6': [1, 2],
        '7': [2, 0],
        '8': [2, 1],
        '9': [2, 2]}
    
    return coord[str(input)]

def askInput(sign):

    providedInput = input('Enter coordinates for %c:' %sign)
    validInput = checkUserInput(providedInput, sign)
    checkedInput = checkRepeatedInputs(validInput, sign)

    if checkedInput not in listOfInputs:
        listOfInputs.append(checkedInput)
    
    if checkedInput in listOfAvailableInputs:
        listOfAvailableInputs.remove(checkedInput)

    return checkedInput

def selectCompInput():

    selectedInput = random.choice(listOfAvailableInputs)

    if selectedInput not in listOfInputs:
        listOfInputs.append(selectedInput)
    
    if selectedInput in listOfAvailableInputs:
        listOfAvailableInputs.remove(selectedInput)

    return selectedInput

def checkUserInput(providedInput, sign):

    if int(providedInput) >= 1 and int(providedInput) <= 9:
        return providedInput

    else:
        print("Incorrect input. Select between 1 --> 9 for %c" %sign)
        return askInput(sign)


def checkRepeatedInputs(providedInput, sign):

    if providedInput in listOfInputs:
        print("Already entered! Select a different location.")
        return askInput(sign)
    
    else:
        return providedInput    

def updateGrid(input, sign, gridMatrix):
    
    Coord = returnCoordinates(input)

    gridMatrix[Coord[0], Coord[1]] = sign

    return gridMatrix

def endGame(gridMatrix):

    if ' ' not in gridMatrix:
        print("It ends in a draw.")
        return False
    
    else:
        return True

def winCondition(sign, gridMatrix):

    for row in range(np.shape(gridMatrix)[0]):

        if np.array_equal(gridMatrix[row, :], np.array([sign, sign, sign])):
            return True
    
    for column in range(np.shape(gridMatrix)[1]):

        if np.array_equal(gridMatrix[:, column], np.array([sign, sign, sign])):
            return True
    
    if np.array_equal(np.diagonal(gridMatrix), np.array([sign, sign, sign])):
            return True
    
    if np.array_equal(np.diagonal(np.fliplr(gridMatrix)), np.array([sign, sign, sign])):
            return True

# %% Define and run main function
def main():

    global listOfInputs, listOfAvailableInputs
    listOfInputs = []
    listOfAvailableInputs = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    print("Let's play tic tac toe!")
    userSign, compSign = chooseSign()
    gridMatrix = makeGrid()
    # showGridMatrix(gridMatrix)

    while endGame(gridMatrix) == True:

        userInput = askInput(userSign)
        gridMatrix = updateGrid(userInput, userSign, gridMatrix)
        showGridMatrix(gridMatrix)

        if winCondition(userSign, gridMatrix):

            print("%s wins the game." %userSign)
            break

        if not endGame(gridMatrix):
            break

        compInput = selectCompInput()
        gridMatrix = updateGrid(compInput, compSign, gridMatrix)
        showGridMatrix(gridMatrix)

        if winCondition(compSign, gridMatrix):
            print("%s wins the game." %compSign)
            break

        print()

if __name__ == '__main__':
    
    main()
