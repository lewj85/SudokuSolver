"""This script solves Sudoku puzzles by parsing their initial html starting state."""

# html values examples
# <INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="659821374843975216271463985482519637937642158516387492365298741728134569194756823">
# <INPUT ID="editmask" TYPE=hidden VALUE="111111110111000011011110001011101010111101111010101110100011110110000111011111111">


##################################################
# CLASSES
##################################################
class PQ:
    def __init__(self):
        self.list = []
        self.top = -1

    # NOTE: push automatically sorts the value by length of its in index 1
    def push(self, value):
        i = 0
        atEnd = True
        if self.top != -1:
            for i in range(self.length()):
                # find the index i where the value should be inserted
                if len(value[1]) < len(self.list[i][1]):
                    atEnd = False
                    break
        # make sure you're not
        if atEnd:
            self.list.append(value)
        else:
            self.list.insert(i, value)
        # don't forget to increment top
        self.top += 1

    def pop(self, index=0):
        if self.top > -1:
            self.top -= 1
            return self.list.pop(index)

    def peek(self, index=0):
        return self.list[index]

    def length(self):
        return self.top + 1

    def show(self):
        for i in range(self.length()):
            print(self.list[i])


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

    ####################################################
    # PART 1 - no guessing
    ####################################################

    print(valueList)
    print(solvedList)
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
            # create a list of values 1-9 for each location on the grid
            for j in range(1, 10):
                sudokuList[i][1].append(j)
        else:
            sudokuList.append([valueList[i], []])

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


    #############################################################
    # while we still haven't solved the puzzle, keep looping
    #############################################################
    m = 0
    while 1 in solvedList:

        # go through each location
        for i in range(81):

            # if there's only 1 possibility left for that location, solve it
            if len(sudokuList[i][1]) == 1:
                print('solving index ' + str(i) + ' - only 1 possibility left')
                solvedList[i] = 0
                #print(sudokuList[i])
                sudokuList[i][0] = sudokuList[i][1][0]
                sudokuList[i][1].pop()
                #print(sudokuList[i])
                #print('found index '+str(i)+': '+str(sudokuList[i][0]))

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
                        #print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexA][1])+'... popping it')
                        sudokuList[indexA][1].pop(sudokuList[indexA][1].index(sudokuList[i][0]))
                    # else:
                    #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexA][1]))

                #######################################################
                # check columns to eliminate possibilities
                #######################################################
                for s in range(9):
                    # go through each row of the current column
                    indexB = (i%9) + (9*s)
                    # pop that value from the list
                    if sudokuList[i][0] in sudokuList[indexB][1]:
                        # print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexB][1])+'... popping it')
                        sudokuList[indexB][1].pop(sudokuList[indexB][1].index(sudokuList[i][0]))
                        # else:
                        #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexB][1]))

                #######################################################
                # check 3x3 sections to eliminate possibilities
                #######################################################
                for u in range(3):
                    for v in range(3):
                        # go through each index of current 3x3 block
                        indexC = ((int(i/3)*3 + u)%9) + (9*v) + (int(i/27)*27)
                        if sudokuList[i][0] in sudokuList[indexC][1]:
                            # print(str(sudokuList[i][0]) + ' is in ' + str(sudokuList[indexB][1])+'... popping it')
                            sudokuList[indexC][1].pop(sudokuList[indexC][1].index(sudokuList[i][0]))
                            # else:
                            #     print(str(sudokuList[i][0])+' is NOT in '+str(sudokuList[indexB][1]))


        # try some more eliminations
        for i in range(81):

            # if solvedList[i] is a known value (is 0), we can expand it
            if not solvedList[i]:

                #######################################################
                # check to see if 5 out of 6 values in adjacent block rows are solved
                #######################################################
                """
                for example
                0 6 5 | 2 9 0 | 0 0 1
                0 0 8 | 1 3 4 | 0 0 0
                7 0 0 | 0 5 0 | 0 0 0
                the bottom left 7 must belong somewhere in 2 9 0 1 3 4 of the next block, and since 5 out of 6
                of them are solved, we know it must belong in the 6th spot
                """
                # first find block it belongs to
                blockNum = 0
                for aa in allBlocks:
                    if i in aa:
                        block = aa
                        break
                    blockNum += 1
                # print(str(i)+' is in block '+str(blockNum))

                # find the 3 blocks in the row
                firstBlock = int(blockNum / 3) * 3
                # print(firstBlock)
                rowBlocks = [firstBlock, firstBlock + 1, firstBlock + 2]
                location = blockNum % 3
                rowBlocks.pop(location)
                # print('other blocks in row are '+str(rowBlocks))

                # isolate the row i is on
                row = int((i % 27) / 9)
                # print(row)

                # check each adjacent block in the row
                for bb in rowBlocks:
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
                        if int((cc % 27) / 9) != row:
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
                                        print('solving index ' + str(x) + ' - 5 out of 6 knowns in adjacent row blocks')
                                        sudokuList[x] = [sudokuList[i], []]
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
                        if cc % 3 != row:
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
                                        sudokuList[x] = [sudokuList[i], []]
                                        solvedList[x] = 0


                # TODO: FIX THIS SECTION
                #######################################################
                # check rows of 3x3 sections to remove possibilities
                #######################################################
                """
                for example
                0 6 5 | 2 9 0 | 0 0 1
                0 0 8 | 1 3 4 | 0 0 0
                1 0 0 | 0 5 0 | 0 0 0
                the top left 6 and the middle 1 3 4 means we can eliminate 6 from the bottom right 3 nodes
                """
                """
                # NOTE: block, rowBlocks, blockNum, row, and col are known from above
                # check each adjacent block in the row
                for bb in rowBlocks:
                    theThree = [[], [], []]

                    # check each value in that block
                    for cc in allBlocks[bb]:
                        # if not on the same row, add to the appropriate list
                        ee = int((cc % 27) / 9)
                        if ee != row:
                            theThree[ee].append(cc)
                            # print(theThree)

                    for ff in range(len(theThree)):
                        counter = 0
                        if theThree[ff]:
                            for gg in theThree[ff]:
                                # if solvedList[cc] is solved (has a 0)
                                if not solvedList[gg]:
                                    counter += 1
                        # print(counter)
                        # if the total count is 3, we can eliminate index i from last row of last rowBlock
                        if counter == 3:
                            temp = rowBlocks
                            temp.remove(bb)
                            lastBlock = temp.pop(0)
                            temp = [0, 1, 2]
                            temp.remove(row)
                            temp.remove(int((gg % 27) / 9))
                            lastRow = temp.pop(0)
                            startIndex = allBlocks[lastBlock][lastRow*3]  # TODO double-check this logic
                            for hh in range(3):
                                try:
                                    sudokuList[startIndex+hh][1].remove(sudokuList[i][0])
                                    print('removed ' + str(i) + ' from ' + str([startIndex, startIndex + 1, startIndex + 2]))
                                except:
                                    print('failed to remove ' + str(i) + ' from ' + str([startIndex, startIndex + 1, startIndex + 2]))
                """

                # TODO: FIX THIS SECTION
                #######################################################
                # check column of 3x3 sections to remove possibilities
                #######################################################
                """
                for ii in colBlocks:
                    theThree = [[], [], []]

                    # check each value in that block
                    for jj in allBlocks[ii]:
                        # if not on the same row, add to the appropriate list
                        kk = jj % 3
                        if kk != row:
                            theThree[kk].append(jj)
                            # print(theThree)

                    for mm in range(len(theThree)):
                        counter = 0
                        if theThree[mm]:
                            for nn in theThree[mm]:
                                # if solvedList[jj] is solved (has a 0)
                                if not solvedList[nn]:
                                    counter += 1
                                # print(counter)
                                # if the total count is 3, we can eliminate index i from last row of last colBlock
                        if counter == 3:
                            temp = colBlocks
                            temp.remove(ii)
                            lastBlock = temp.pop(0)
                            temp = [0, 1, 2]
                            temp.remove(col)
                            print(col)
                            print(nn % 3)
                            temp.remove(nn % 3)
                            lastCol = temp.pop(0)
                            startIndex = allBlocks[lastBlock][lastCol]
                            for pp in [0, 9, 18]:
                                try:
                                    sudokuList[startIndex+pp][1].remove(sudokuList[i][0])
                                    print('removed ' + str(i) + ' from ' + str([startIndex, startIndex + 9, startIndex + 18]))
                                except:
                                    print('failed to remove ' + str(i) + ' from ' + str([startIndex, startIndex + 9, startIndex + 18]))
                """


                #######################################################
                # check to see if 2 out of 3 row blocks have a value AND the 3rd block has 2 out of 3 values solved in that row
                #######################################################
                """
                for example
                0 3 0 | 0 1 0 | 8 0 9
                0 0 6 | 4 9 0 | 0 1 0
                0 0 1 | 0 0 2 | 3 0 4
                the top left 3 and bottom right 3 mean the middle row of middle block must contain a 3
                and since 2 out of 3 of those values are solved (4 9 0), we know the 3rd must be a 3
                """

                #######################################################
                # check to see if 2 out of 3 column blocks have a value AND the 3rd block has 2 out of 3 values solved in that column
                #######################################################



        # TODO remove m, used for debugging. instead just compare previous state to current state. if same then break
        m += 1
        if m > 50:
            break


        ####################################################
        # PART 2 - guessing (aka "Magic")
        ####################################################

        # add items to priority queue
        pq = PQ()
        for i in range(81):
            pq.push(sudokuList[i])
        # pq.show()

        # 2nd while loop uses a pathing algorithm to look at possibilities
        # NOTE: it uses a priority queue to expand the most likely nodes first
        # NOTE: it marks guessed nodes as '2' in solvedList
        while 1 in solvedList or 2 in solvedList:

            # remove all values from priority queue that have a length of 0 (ie. they are solved)
            for i in range(pq.length()):
                if len(pq.peek(0)[1]) == 0:  # NOTE: always peek(0), not peek(i) because we are popping
                    pq.pop()
                else:
                    break  # stop early to save processing time
            # pq.show()

            # TODO: magic

            break


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


def checkPuzzle(puzzle1, puzzle2):
    counter = 0
    for i in range(81):
        counter += (puzzle1[i]==puzzle2[i])
    #return (counter == 81)
    return counter


def main():

    # TODO remove these samples, used for debugging
    values = "659821374843975216271463985482519637937642158516387492365298741728134569194756823"
    solved = "111111110111000011011110001011101010111101111010101110100011110110000111011111111"
    # change this   ^   to a 0 and the whole puzzle can already be solved!

    # regex
    parseHTML('blah')

    # first print the puzzle unsolved
    printPuzzle(values, solved)

    # solve the puzzle
    result = solvePuzzle(values, solved)

    # print the solved puzzle
    printPuzzle(result)

    # double check all values are correct
    print(checkPuzzle(result, values))


if __name__ == "__main__":
    main()

