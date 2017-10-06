"""This script solves Sudoku puzzles by parsing their initial html starting state."""
# html values examples
# <INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="659821374843975216271463985482519637937642158516387492365298741728134569194756823">
# <INPUT ID="editmask" TYPE=hidden VALUE="111111110111000011011110001011101010111101111010101110100011110110000111011111111">

def printPuzzle(valueList, solvedList):
    for i in range(9):
        lineVals = []
        for j in range(9):
            index = (i * 9) + j
            if not int(solvedList[index]):
                lineVals.append(int(valueList[index]))
            else:
                lineVals.append(0)
        print(lineVals)


def parseHTML(htmlStuff):
    # regex is fun
    pass


def solvePuzzle(valueList, solvedList):

    # create a list of values 1-9 for each location on the grid
    vals = []
    sudokuList = []
    for i in range(9):
        vals.append(i+1)

    # convert the lists to ints
    temp = []
    temp2 = []
    for i in range(81):
        temp.append(int(valueList[i]))
        temp2.append(int(solvedList[i]))

    valueList = temp
    solvedList = temp2
    del temp, temp2

    for i in range(81):
        if solvedList[i]:
            sudokuList.append([0, vals])
        else:
            sudokuList.append([valueList[i], []])

    print(sudokuList)
    m = 0

    # while we still haven't solved the puzzle, keep looping
    while 1 in solvedList:

        # find each unsolved value
        for i in range(81):
            if solvedList[i]:
                # first check row to eliminate possibilities
                for r in range(9):
                    index = int(i/9) + r  # this goes through each column of the current row
                    if sudokuList[i][0] in sudokuList[index][1]:
                        for j in range(len(sudokuList[index][1])):
                            if sudokuList[index][1][j] == sudokuList[i][0]:
                                sudokuList[index][1][j] = ''
                # then check columns to eliminate possibilities
                for c in range(0, 81, 9):
                    pass

                # then check 3x3 sections to eliminate possibilities

        m += 1
        if m > 200:
            break
    print(sudokuList)




def main():

    values = "659821374843975216271463985482519637937642158516387492365298741728134569194756823"
    solved = "111111110111000011011110001011101010111101111010101110100011110110000111011111111"

    parseHTML('blah')

    solvePuzzle(values, solved)

    printPuzzle(values, solved)


main()

