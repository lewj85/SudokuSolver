"""This script solves Sudoku puzzles by parsing their initial html starting state."""
# html values examples
# <INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="659821374843975216271463985482519637937642158516387492365298741728134569194756823">
# <INPUT ID="editmask" TYPE=hidden VALUE="111111110111000011011110001011101010111101111010101110100011110110000111011111111">

def printPuzzle(valueList, solvedList='0'*81):
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

    print(valueList)
    print(solvedList)
    # create a list of values 1-9 for each location on the grid
    sudokuList = []

    # convert the lists to ints
    temp = []
    temp2 = []
    for i in range(81):
        temp.append(int(valueList[i]))
        temp2.append(int(solvedList[i]))
    valueList = temp
    solvedList = temp2
    del temp, temp2

    # fill starting matrix/list with known values
    for i in range(81):
        if solvedList[i]:
            sudokuList.append([0, []])
            for j in range(1, 10):
                sudokuList[i][1].append(j)
        else:
            sudokuList.append([valueList[i], []])

    m = 0
    # while we still haven't solved the puzzle, keep looping
    while 1 in solvedList:

        # go through each location
        for i in range(81):

            # if there's only 1 possibility left for that location, solve it
            if len(sudokuList[i][1]) == 1:
                solvedList[i] = 0
                #print(sudokuList[i])
                sudokuList[i][0] = sudokuList[i][1][0]
                sudokuList[i][1].pop(0)
                #print(sudokuList[i])
                #print('found index '+str(i)+': '+str(sudokuList[i][0]))

            # expand each solved value
            if not solvedList[i]:

                # check rows to eliminate possibilities
                for r in range(9):
                    # go through each column of the current row
                    indexA = int(i/9)*9 + r
                    # pop that value from the list
                    if sudokuList[i][0] in sudokuList[indexA][1]:
                        #print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexA][1])+'... popping it')
                        sudokuList[indexA][1].pop(sudokuList[indexA][1].index(sudokuList[i][0]))
                    # else:
                    #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexA][1]))


                # check columns to eliminate possibilities
                for s in range(9):
                    # go through each row of the current column
                    indexB = (i%9) + (9*s)
                    # pop that value from the list
                    if sudokuList[i][0] in sudokuList[indexB][1]:
                        # print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexB][1])+'... popping it')
                        sudokuList[indexB][1].pop(sudokuList[indexB][1].index(sudokuList[i][0]))
                        # else:
                        #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexB][1]))


                # check 3x3 sections to eliminate possibilities
                for u in range(3):
                    for v in range(3):
                        # go through each column of the current row
                        indexC = ((int(i/3)*3 + u)%9) + (9*v) + (int(i/27)*27)
                        if sudokuList[i][0] in sudokuList[indexC][1]:
                            # print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexB][1])+'... popping it')
                            sudokuList[indexC][1].pop(sudokuList[indexC][1].index(sudokuList[i][0]))
                            # else:
                            #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexB][1]))

        # TODO remove m, used for debugging
        m += 1
        if m > 20:
            break

    finalList = ''
    newList = ''
    for i in range(81):
        finalList+=str(sudokuList[i][0])
        newList+=str(solvedList[i])

    print(finalList)
    print(newList)


    # 2nd while loop uses a pathing algorithm to look at possibilities
    # NOTE: it uses a priority queue to expand the most likely nodes first
    # NOTE: it marks guessed nodes as '2' in solvedList
    while 1 in solvedList or 2 in solvedList:

        # magic

        break



    return finalList


def checkPuzzle(puzzle1, puzzle2):
    counter = 0
    for i in range(81):
        counter += (puzzle1[i]==puzzle2[i])
    return (counter == 81)


def main():

    # TODO remove these samples, used for debugging
    values = "659821374843975216271463985482519637937642158516387492365298741728134569194756823"
    solved = "111111110111000011011110001011101010111101111010101110100011110110000111011111111"

    # first print the puzzle unsolved
    printPuzzle(values, solved)

    # regex
    parseHTML('blah')

    # solve the puzzle
    result = solvePuzzle(values, solved)

    # print the solved puzzle
    printPuzzle(result)

    # double check all values are correct
    print(checkPuzzle(result, values))


if __name__ == "__main__":
    main()
