"""This script solves Sudoku puzzles by parsing their initial html starting state."""

# html values examples
# <INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="659821374843975216271463985482519637937642158516387492365298741728134569194756823">
# <INPUT ID="editmask" TYPE=hidden VALUE="111111110111000011011110001011101010111101111010101110100011110110000111011111111">

"""
for reference:
 0  1  2 |  3  4  5 |  6  7  8
 9 10 11 | 12 13 14 | 15 16 17
18 19 20 | 21 22 23 | 24 25 26
------------------------------
27 28 29 | 30 31 32 | 33 34 35
36 37 38 | 39 40 41 | 42 43 44
45 46 47 | 48 49 50 | 51 52 53
------------------------------
54 55 56 | 57 58 59 | 60 61 62
63 64 65 | 66 67 68 | 69 70 71
72 73 74 | 75 76 77 | 78 79 80
"""


##################################################
# FUNCTIONS
##################################################
def parseHTML(htmlStuff):
    # regex is fun
    pass


def printPuzzle(valueList, solvedList='0'*81):
    for i in range(9):
        if i in [3, 6]:
            print('-'*22)
        lineVals = ''
        for j in range(9):
            if j in [3, 6]:
                lineVals += '| '
            index = (i * 9) + j
            if not int(solvedList[index]):
                lineVals += valueList[index]+' '
            else:
                lineVals += '0 '
        print(lineVals)


def solvePuzzle(valueList, solvedList):

    print(valueList)
    print(solvedList)
    sudokuList = []

    # convert the lists to ints
    temp1 = []
    temp2 = []
    for i in range(81):
        temp1.append(int(valueList[i]))
        temp2.append(int(solvedList[i]))
    valueList = temp1
    solvedList = temp2
    del temp1, temp2

    # fill starting matrix/list with known values
    for i in range(81):
        if solvedList[i]:
            sudokuList.append([0, [], i])
            # create a list of values 1-9 for each location on the grid
            for j in range(1, 10):
                sudokuList[i][1].append(j)
        else:
            sudokuList.append([valueList[i], [], i])

    # list of block indices
    block0 = [0, 9, 18, 1, 10, 19, 2, 11, 20]
    block1 = [x + 3 for x in block0]
    block2 = [x + 3 for x in block1]
    block3 = [x + 27 for x in block0]
    block4 = [x + 27 for x in block1]
    block5 = [x + 27 for x in block2]
    block6 = [x + 27*2 for x in block0]
    block7 = [x + 27*2 for x in block1]
    block8 = [x + 27*2 for x in block2]
    allBlocks = [block0, block1, block2, block3, block4, block5, block6, block7, block8]
    #for i in allBlocks:
    #    print(i)


    ####################################################
    # PART 1 - no guessing
    ####################################################

    # keep looping until we solve the puzzle - set max loops
    loops = 10
    while loops and 1 in solvedList:
        loops -= 1

        solveLocation1(sudokuList, solvedList)
        removePossibilities1(sudokuList, solvedList)
        solveLocation2(sudokuList, solvedList)
        solveLocation1(sudokuList, solvedList)
        removePossibilities2(sudokuList, solvedList, allBlocks)
        solveLocation2(sudokuList, solvedList)
        solveLocation1(sudokuList, solvedList)
        removePossibilities3(sudokuList, solvedList, allBlocks)
        solveLocation2(sudokuList, solvedList)

    ####################################################
    # PART 2 - guessing (aka "Magic")
    ####################################################
    # check to see if it's solved already
    if 1 in solvedList:
        # otherwise sort any unguessed nodes by the number of their possibilities
        guessList = sorted(sudokuList, key=lambda x: len(x[1]))
        # and guess the values
        recursions = 0
        dynamicProgrammingList = []
        sudokuList, solvedList, guessList = guessValues(sudokuList, solvedList, guessList, allBlocks, recursions, dynamicProgrammingList)


    finalList = ''
    newList = ''
    for i in range(81):
        finalList += str(sudokuList[i][0])
        newList += str(solvedList[i])

    print(finalList)
    print(newList)

    solvedList2 = ''
    for abc in range(81):
        solvedList2 += str(len(sudokuList[abc][1]))
    print(solvedList2)

    return finalList


def solveLocation1(sudokuList, solvedList):
    # go through each location
    for i in range(81):

        # if there's only 1 possibility left for that location, solve it
        if len(sudokuList[i][1]) == 1:
            print('solving index ' + str(i) + ' - only 1 possibility left')
            solvedList[i] = 0
            # print(sudokuList[i])
            sudokuList[i][0] = sudokuList[i][1][0]
            sudokuList[i][1].pop()
            # print(sudokuList[i])
            # print('found index '+str(i)+': '+str(sudokuList[i][0]))


def solveLocation2(sudokuList, solvedList):
    #######################################################
    # check to see if 2 out of 3 row blocks have a value AND the 3rd block has 2 out of 3 values solved in that row
    #######################################################
    """
    for example
    1 0 0 | 0 0 0 | 0 0 0
    0 0 0 | 0 2 3 | 0 0 0
    0 0 0 | 0 0 0 | 1 0 0
    the top left 1 and bottom right 1 mean the middle row of middle block must contain a 1
    and since 2 out of 3 of those values are solved (0 2 3), we know the 3rd must be a 1
    """
    # easiest way to do this is simply to check if each location has a 'unique possibility'
    for i in range(81):

        earlyBreak = False

        #######################################################
        # check rows for unique possibilities
        #######################################################
        if solvedList[i]:
            for j in range(len(sudokuList[i][1])):
                counter = 0

                # go through each column of the current row
                for r in range(9):
                    indexA = int(i / 9) * 9 + r

                    # print('i = ' + str(i))
                    # print('j = ' + str(j))
                    # print('indexA = ' + str(indexA))
                    # print('sudokuList[i] = ' + str(sudokuList[i]))
                    # print('sudokuList[indexA] = ' + str(sudokuList[indexA]))

                    # this shouldn't happen, but adding it in to be safe - make sure the value isn't already solved
                    if sudokuList[i][1][j] == sudokuList[indexA][0]:
                        #print('removing possibility ' + str(sudokuList[indexA][0]) + ' from ' + str(sudokuList[i]) + ' at index ' + str(i))
                        sudokuList[i][1].pop(j)
                        earlyBreak = True
                        break

                    # count up each time that possibility is found
                    if sudokuList[i][1][j] in sudokuList[indexA][1]:
                        # print(str(sudokuList[i][1][j] in sudokuList[indexA][1]))
                        counter += 1

                if earlyBreak:
                    break

                # if only one possibility was found, we know it was in the current cell, so solve it
                if counter == 1:
                    print('solving index '+str(i)+' - the row has no similar possibilities')
                    solvedList[i] = 0
                    sudokuList[i][0] = sudokuList[i][1][j]
                    sudokuList[i][1] = []
                    break

        #######################################################
        # check columns for unique possibilities
        #######################################################
        if solvedList[i]:  # check again, because it may have just been solved above
            for j in range(len(sudokuList[i][1])):
                counter = 0

                # go through each column of the current row
                for c in range(9):
                    indexB = (i % 9) + (9 * c)

                    # this shouldn't happen, but adding it in to be safe - make sure the value isn't already solved
                    if sudokuList[i][1][j] == sudokuList[indexB][0]:
                        #print('removing possibility ' + str(sudokuList[indexB][0]) + ' from ' + str(sudokuList[i]) + ' at index ' + str(i))
                        sudokuList[i][1].pop(j)
                        earlyBreak = True
                        break

                    # count up each time that possibility is found
                    if sudokuList[i][1][j] in sudokuList[indexB][1]:
                        counter += 1

                if earlyBreak:
                    break

                # if only one possibility was found, we know it was in the current cell, so solve it
                if counter == 1:
                    print('solving index '+str(i)+' - the column has no similar possibilities')
                    solvedList[i] = 0
                    sudokuList[i][0] = sudokuList[i][1][j]
                    sudokuList[i][1] = []
                    break

        #######################################################
        # check 3x3 blocks for unique possibilities
        #######################################################
        if solvedList[i]:  # check again, because it may have just been solved above
            for j in range(len(sudokuList[i][1])):
                counter = 0

                # go through each column of the current row
                for u in range(3):
                    for v in range(3):
                        # go through each index of current 3x3 block
                        indexC = ((int(i / 3) * 3 + u) % 9) + (9 * v) + (int(i / 27) * 27)

                        # this shouldn't happen, but adding it in to be safe - make sure the value isn't already solved
                        if sudokuList[i][1][j] == sudokuList[indexC][0]:
                            #print('removing possibility ' + str(sudokuList[indexC][0]) + ' from ' + str(sudokuList[i]) + ' at index ' + str(i))
                            sudokuList[i][1].pop(j)
                            earlyBreak = True
                            break

                        # count up each time that possibility is found
                        if sudokuList[i][1][j] in sudokuList[indexC][1]:
                            counter += 1

                    if earlyBreak:
                        break

                if earlyBreak:
                    break

                # if only one possibility was found, we know it was in the current cell, so solve it
                if counter == 1:
                    print('solving index '+str(i)+' - the 3x3 block has no similar possibilities')
                    solvedList[i] = 0
                    sudokuList[i][0] = sudokuList[i][1][j]
                    sudokuList[i][1] = []
                    break


def removePossibilities1(sudokuList, solvedList):
    # go through each location
    for i in range(81):

        ########################################
        # expand each solved value
        ########################################
        # if solvedList[i] is 0, it means it is solved, so it can be expanded
        if not solvedList[i]:

            #######################################################
            # check rows to eliminate possibilities
            #######################################################
            for r in range(9):
                # go through each column of the current row
                indexA = int(i/9)*9 + r
                # pop that value from the list
                if sudokuList[i][0] in sudokuList[indexA][1]:
                    #print('removing possibility ' + str(sudokuList[i][0]) + ' from ' + str(sudokuList[indexA]) + ' at index ' + str(indexA))
                    sudokuList[indexA][1].pop(sudokuList[indexA][1].index(sudokuList[i][0]))

            #######################################################
            # check columns to eliminate possibilities
            #######################################################
            for s in range(9):
                # go through each row of the current column
                indexB = (i % 9) + (9 * s)
                # pop that value from the list
                if sudokuList[i][0] in sudokuList[indexB][1]:
                    #print('removing possibility ' + str(sudokuList[i][0]) + ' from ' + str(sudokuList[indexB]) + ' at index ' + str(indexB))
                    sudokuList[indexB][1].pop(sudokuList[indexB][1].index(sudokuList[i][0]))

            #######################################################
            # check 3x3 sections to eliminate possibilities
            #######################################################
            for u in range(3):
                for v in range(3):
                    # go through each index of current 3x3 block
                    indexC = ((int(i / 3) * 3 + u) % 9) + (9 * v) + (int(i / 27) * 27)
                    if sudokuList[i][0] in sudokuList[indexC][1]:
                        #print('removing possibility ' + str(sudokuList[i][0]) + ' from ' + str(sudokuList[indexC]) + ' at index ' + str(indexC))
                        sudokuList[indexC][1].pop(sudokuList[indexC][1].index(sudokuList[i][0]))


def removePossibilities2(sudokuList, solvedList, allBlocks):
    # try some more eliminations
    for i in range(81):

        # if solvedList[i] is a known value (is 0), we can expand it
        if not solvedList[i]:

            #######################################################
            # check to see if 5 out of 6 values in adjacent block rows are solved
            #######################################################
            """
            for example
            1 0 0 | 0 0 0 | 0 0 0
            0 0 0 | 2 3 4 | 0 0 0
            0 0 0 | 5 6 0 | 0 0 0
            the top right 1 must belong somewhere in 2 3 4 5 6 0 of the middle block, and since 5 out of 6
            of them are solved in that middle block, we know the 1 must belong in the 6th spot
            """
            # first find block it belongs to
            blockNum = 0
            for aa in allBlocks:
                if i in aa:
                    block = aa
                    break
                blockNum += 1
            #print(str(i)+' is in block '+str(blockNum)+' with values '+str(block))

            # find the 3 blocks in the row
            firstBlock = int(blockNum / 3) * 3
            # print(firstBlock)
            rowBlocks = [firstBlock, firstBlock + 1, firstBlock + 2]
            location = blockNum % 3
            rowBlocks.pop(location)
            #print('other blocks in row are '+str(rowBlocks))

            # isolate the row i is on
            row = int((i % 27) / 9)
            #print(str(i)+' is in row '+str(row))

            # check each adjacent block in the row
            for bb in rowBlocks:
                counter = 0
                theSix = []
                # store the solved numbers in the current block
                blockVals = []
                for dd in allBlocks[bb]:
                    blockVals.append(sudokuList[dd][0])
                #print(blockVals)

                # check each value in that block
                for cc in allBlocks[bb]:
                    # if not on the same row, add up solved values
                    # print('is row '+str(int((int(cc/9)*9 % 27)/9))+' != '+str(row))
                    if int((cc % 27) / 9) != row:
                        # print('appending '+str(cc)+' to theSix')
                        theSix.append(cc)
                        # print(theSix)
                        # if solvedList[cc] is solved (has a 0)
                        if not solvedList[cc]:
                            counter += 1
                    #print(counter)
                    # if the total count is 5, we can solve the 6th
                    if counter == 5:
                        #print('theSix for ' + str(i) + ' are ' + str(theSix))
                        for x in theSix:
                            # find the index that's unsolved and make sure the value doesn't already exist in the block
                            if solvedList[x]:
                                #print(str(x)+' needs to be solved')
                                #print('checking to see if '+str(sudokuList[i][0])+' is in '+str(blockVals))
                                if sudokuList[i][0] not in blockVals:
                                    # replace the unknown with sudokuList[i] and update solvedList
                                    print('solving index ' + str(x) + ' - 5 out of 6 knowns in adjacent row blocks')
                                    sudokuList[x] = sudokuList[i]
                                    solvedList[x] = 0


            #######################################################
            # check to see if 5 out of 6 values in adjacent block rows are solved
            #######################################################
            # NOTE: blockNum was determined above and can be used again below

            # find the 3 blocks in the column
            firstBlock = blockNum % 3
            colBlocks = [firstBlock, firstBlock + 3, firstBlock + 6]
            location = int(blockNum / 3)
            colBlocks.pop(location)
            # print('other blocks in row are '+str(rowBlocks))

            # store the solved numbers in the current block
            blockVals = []
            for aa in block:
                blockVals.append(sudokuList[aa])
            #print(blockVals)

            # isolate the column i is on
            col = i % 3

            # check each adjacent block in the row
            for bb in colBlocks:
                counter = 0
                theSix = []
                # store the solved numbers in the current block
                blockVals = []
                for dd in block:
                    blockVals.append(sudokuList[dd][0])
                # print(blockVals)

                # check each value in that block
                for cc in allBlocks[bb]:
                    # if not on the same row, add up solved values
                    # print('is row '+str(int((int(cc/9)*9 % 27)/9))+' != '+str(row))
                    if cc % 3 != col:
                        # print('appending '+str(cc)+' to theSix')
                        theSix.append(cc)
                        # print(theSix)
                        # if solvedList[cc] is solved (has a 0)
                        if not solvedList[cc]:
                            counter += 1
                    # print(counter)
                    # if the total count is 5, we can solve the 6th
                    if counter == 5:
                        #print('theSix for ' + str(i) + ' are ' + str(theSix))
                        for x in theSix:
                            # find the index that's unsolved and make sure the value doesn't already exist in the block
                            if solvedList[x]:
                                #print(str(x)+' needs to be solved')
                                if sudokuList[i][0] not in blockVals:
                                    # replace the unknown with sudokuList[i] and update solvedList
                                    print('solving index ' + str(x) + ' - 5 out of 6 knowns in adjacent column blocks')
                                    sudokuList[x] = sudokuList[i]
                                    solvedList[x] = 0


def removePossibilities3(sudokuList, solvedList, allBlocks):
    # check all locations
    for i in range(81):

        # if solvedList[i] is a known value (is 0), we can expand it
        if not solvedList[i]:

            #######################################################
            # check rows of 3x3 sections to remove possibilities
            #######################################################
            """
            for example
            1 0 0 | 0 0 0 | 0 0 0
            0 0 0 | 2 3 4 | 0 0 0
            0 0 0 | 0 0 0 | 0 0 0
            the top left 1 and the middle 2 3 4 means we can eliminate 1 from the bottom right 3 nodes
            """
            # first find block it belongs to
            blockNum = 0
            for block in allBlocks:
                if i in block:
                    break
                blockNum += 1
            # print(str(i)+' is in block '+str(blockNum)+' with values '+str(block))

            # find the 3 blocks in the row
            firstBlock = int(blockNum / 3) * 3
            # print(firstBlock)
            rowBlocks = [firstBlock, firstBlock + 1, firstBlock + 2]  # blocks [0,1,2] or [3,4,5] or [6,7,8]
            location = blockNum % 3  # get index of current block to pop out of rowBlocks below
            rowBlocks.pop(location)
            # print('other blocks in row are '+str(rowBlocks))

            # isolate the row i is on
            row = int((i % 27) / 9)
            # print(str(i)+' is in row '+str(row))

            # check each adjacent block in the row
            for rowBlockNum in rowBlocks:
                theThree = [[], [], []]

                # check each value in that block
                for threeIndex in allBlocks[rowBlockNum]:
                    # if not on the same row, add the index to the appropriate list
                    diffRow = int((threeIndex % 27) / 9)
                    if diffRow != row:
                        theThree[diffRow].append(threeIndex)
                #print('i is ' + str(i) + ' : theThree is ' + str(theThree))

                for eachThree in range(len(theThree)):
                    counter = 0
                    if theThree[eachThree]:  # because one will be an empty list
                        for threeIndex in theThree[eachThree]:
                            # if solvedList[threeIndex] is solved (has a 0)
                            # bugfix: make sure sudokuList[i][0] isn't in theThree indices
                            if not solvedList[threeIndex] and sudokuList[i][0] != sudokuList[threeIndex][0]:
                                counter += 1
                    # print(counter)
                    # if the total count is 3, we can eliminate index i from last row of last rowBlock
                    #print(rowBlocks)
                    if counter == 3:
                        temp = rowBlocks[:]  # NOTE: need [:] to make a copy, otherwise python will just make another reference for the same object...
                        temp.remove(rowBlockNum)
                        lastBlock = temp.pop(0)
                        #print('lastBlock is '+str(lastBlock))
                        temp = [0, 1, 2]
                        temp.remove(row)
                        temp.remove(int((threeIndex % 27) / 9))
                        lastRow = temp.pop(0)
                        startIndex = allBlocks[lastBlock][lastRow]  # takes index 0,1, or 2 because the lastBlock row order is [0,1,2...]
                        # print('i is ' + str(i) + ' with value '+str(sudokuList[i]))
                        # print('theThree is ' + str(theThree))
                        # print('threeIndex is '+str(threeIndex))
                        # print('lastRow is '+str(lastRow))
                        # print('allBlocks[lastBlock] is '+str(allBlocks[lastBlock]))
                        # print('startIndex is ' + str(startIndex))
                        for k in [0,1,2]:
                            #print('sudokuList[startIndex+k] is ' + str(sudokuList[startIndex + k]))
                            try:
                                sudokuList[startIndex+k][1].remove(sudokuList[i][0])
                                #print('removed possibility of ' + str(sudokuList[i][0]) + ' from index ' + str(startIndex+k))
                            except:
                                #print('failed to remove possibility of ' + str(sudokuList[i][0]) + ' from index ' + str(startIndex+k))
                                pass


            #######################################################
            # check column of 3x3 sections to remove possibilities
            #######################################################
            # find the 3 blocks in the column
            firstBlock = blockNum % 3
            colBlocks = [firstBlock, firstBlock + 3, firstBlock + 6]  # blocks [0,3,6] or [1,4,7] or [2,5,8]
            location = int(blockNum / 3)  # get index of current block to pop out of colBlocks below
            colBlocks.pop(location)
            #print('other blocks in col are '+str(colBlocks))

            # isolate the column i is on: 0, 1, or 2
            col = i % 3
            #print(str(i)+' is in column '+str(col))
            for block in colBlocks:
                theThree = [[], [], []]

                # check each value in that block
                for threeIndex in allBlocks[block]:
                    # if not on the same row, add to the appropriate list
                    diffCol = threeIndex % 3
                    if diffCol != col:
                        theThree[diffCol].append(threeIndex)
                        # print(theThree)

                for eachThree in range(len(theThree)):
                    counter = 0
                    if theThree[eachThree]:  # because one index will be an empty list
                        for threeIndex in theThree[eachThree]:
                            # if solvedList[jj] is solved (has a 0)
                            if not solvedList[threeIndex] and sudokuList[i][0] != sudokuList[threeIndex][0]:
                                counter += 1
                            # print(counter)
                            # if the total count is 3, we can eliminate index i from last row of last colBlock
                    if counter == 3:
                        temp = colBlocks[:]  # NOTE: we need to put [:] or python will reference the same object
                        temp.remove(block)
                        lastBlock = temp.pop(0)
                        temp = [0, 1, 2]
                        temp.remove(col)
                        temp.remove(threeIndex % 3)
                        lastCol = temp.pop(0)
                        startIndex = allBlocks[lastBlock][lastCol*3]  # we want to take 0, 1, or 2 and get index 0, 3, or 6, so multiply by 3
                        for k in [0, 9, 18]:  # add 0, 9, and 18 to get column indices from the starting index
                            #print('sudokuList[startIndex+k] is ' + str(sudokuList[startIndex+k]))
                            try:
                                sudokuList[startIndex+k][1].remove(sudokuList[i][0])
                                #print('removed possibility of ' + str(sudokuList[i][0]) + ' from indices ' + str([startIndex, startIndex + 9, startIndex + 18]))
                            except:
                                #print('failed to remove possibility of ' + str(sudokuList[i][0]) + ' from indices ' + str([startIndex, startIndex + 9, startIndex + 18]))
                                pass


def guessValues(sudokuList2, solvedList2, guessList2, allBlocks, recursions, dynamicProgammingList):
    ####################################################
    # PART 2 - guessing (aka "Magic")
    ####################################################
    # base case
    if 1 not in solvedList2:
        #print('base case')
        return sudokuList2, solvedList2, guessList2

    # create copies for recursion so we can undo changes if need be
    sudokuListCopy = sudokuList2[:]
    solvedListCopy = solvedList2[:]
    guessListCopy = guessList2[:]

    # sort the remaining items by their remaining possibilities
    guessListCopy.sort(key=lambda x: len(x[1]))

    # remove all values from guessList that have no guesses remaining (ie. they are solved)
    while not guessListCopy[0][1]:
        guessListCopy.pop(0)
    #print(guessList)

    # explore the next node
    node = guessListCopy.pop(0)
    #print('node is ' + str(node))

    # guess values
    for i in range(len(node[1])):

        sudokuListCopy[node[2]] = [node[1][i], [], node[2]]
        solvedListCopy[node[2]] = 2

        removePossibilities1(sudokuListCopy, solvedListCopy)
        removePossibilities2(sudokuListCopy, solvedListCopy, allBlocks)

        # TODO: add a better guessValues algorithm because even with dynamic programming, 20+ unknowns takes forever - try MCTS
        # NOTE: DP doesn't seem to be triggering and all it does it take up space in memory, so removing it for now...
        #if sudokuListCopy not in dynamicProgammingList:
        #print(sudokuListCopy)
        #temp = sudokuListCopy[:]
        #dynamicProgammingList.append(temp)
        #del temp
        #print(len(dynamicProgammingList))
        recursions += 1
        possibleSudoku, possibleSolved, possibleGuess = guessValues(sudokuListCopy, solvedListCopy, guessListCopy, allBlocks, recursions, dynamicProgammingList)
        #if recursions < 33:
        print('recursion depth: ' + recursions*'*')
        copiesAreOkay = testForDuplicates(possibleSudoku)
        #print(copiesAreOkay)
        if copiesAreOkay:
            #print('found solution')
            return possibleSudoku, possibleSolved, possibleGuess
        #else:
        #    print('yay for DP')

    # either dynamic programming prevented the check or none of the guesses were viable, so return original lists
    #print('DP or exhausted')
    return sudokuList2, solvedList2, guessList2


def testForDuplicates(possibleSolution):

    for i in range(81):

        # go through each index of current row
        for r in range(9):
            indexA = int(i / 9) * 9 + r
            if possibleSolution[i][0] == possibleSolution[indexA][0]:
                if i != indexA:  # skip current index
                    return False

        # go through each index of current column
        for c in range(9):
            indexB = (i % 9) + (9 * c)
            if possibleSolution[i][0] == possibleSolution[indexB][0]:
                if i != indexB:  # skip current index
                    return False

        # go through each index of current 3x3 block
        for u in range(3):
            for v in range(3):
                indexC = ((int(i / 3) * 3 + u) % 9) + (9 * v) + (int(i / 27) * 27)
                if possibleSolution[i][0] == possibleSolution[indexC][0]:
                    if i != indexC:  # skip current index
                        return False

    # otherwise no collisions so return True
    return True


def checkPuzzle(puzzle1, puzzle2):
    counter = 0
    for i in range(81):
        counter += (puzzle1[i]==puzzle2[i])
    #return (counter == 81)
    return counter


def main():

    # TODO remove these samples, used for debugging
    values = "659821374843975216271463985482519637937642158516387492365298741728134569194756823"
    #solved = "111111110111000011011110001011101010111101111010101110100011110110000111011111111"  # 81/81
    solved = "010000100001010001010010001000000000111000000000000000100000100100000101010000001"  # 63/81
    #solved = "000000000000000000000000000000000000000000000000000000000000000000111111111111111"


    # regex
    parseHTML('blah')

    # first print the puzzle unsolved
    printPuzzle(values, solved)

    # solve the puzzle
    result = solvePuzzle(values, solved)

    # print the solved puzzle
    printPuzzle(result)

    # double check all values are correct
    print('Values solved: ' + str(checkPuzzle(result, values)) + '/81.')


if __name__ == "__main__":
    main()

