import copy
import pdb
import pprint
import time
pp = pprint.PrettyPrinter(indent=4)

BLOCKER_BLOCK = 100
CHANGER_BLOCK_BLOCKING = 101
CHANGER_BLOCK_UNBLOCKING = 102

def numRowsInCol( puzzleBoard, col):
    count = 0
    for row in range(0, len(puzzleBoard)):
        if puzzleBoard[row][col] != 0 and puzzleBoard[row][col] != CHANGER_BLOCK_UNBLOCKING:
            count += 1
    return count

def getBottomRow( puzzleBoard ):
    bottomRow = copy.copy(puzzleBoard[0])
    for row in range(1, len(puzzleBoard)):
        for col in range(0, 5):
            if puzzleBoard[row][col] != 0 and puzzleBoard[row][col] != CHANGER_BLOCK_UNBLOCKING:
                bottomRow[col] = puzzleBoard[row][col]
    return bottomRow

def switchChangerBlocks( puzzleBoard ):
    for row in range(0, len(puzzleBoard)):
        for col in range(0, 5):
            if puzzleBoard[row][col] == CHANGER_BLOCK_BLOCKING:
                puzzleBoard[row][col] = CHANGER_BLOCK_UNBLOCKING
            elif puzzleBoard[row][col] == CHANGER_BLOCK_UNBLOCKING:
                puzzleBoard[row][col] = CHANGER_BLOCK_BLOCKING

def removeBlockerBlocks( puzzleBoard ):
    for row in range(0, len(puzzleBoard)):
        hasBlockerBlock = False
        for col in range(0, 5):
            if puzzleBoard[row][col] == BLOCKER_BLOCK:
                hasBlockerBlock = True
                break;

        if hasBlockerBlock:
            isRowClear = True
            for col in range(0, 5):
                if bottomRow[i] != 0 and bottomRow[i] != BLOCKER_BLOCK and bottomRow[i] != CHANGER_BLOCK_BLOCKING and bottomRow[i] != CHANGER_BLOCK_UNBLOCKING:
                    isRowClear = False
                    break;

            if isRowClear:
                for col in range(0, 5):
                    if puzzleBoard[row][col] == BLOCKER_BLOCK:
                        puzzleBoard[row][col] = 0

def isPuzzleDead( puzzleBoard, curRemoveType):
    bottomRow = getBottomRow(puzzleBoard)
    foundPossibleTake = False
    for i in range(0, 5):
        if bottomRow[i] != 0 and bottomRow[i] != BLOCKER_BLOCK and bottomRow[i] != CHANGER_BLOCK_BLOCKING:
            foundPossibleTake = True
            break
    
    if not foundPossibleTake:
        return True

    if curRemoveType == 0:
        return False

    for i in range(0, 5):
        if bottomRow[i] == curRemoveType:
            return False
    return True

def performTake( takeAt, puzzleBoard):
    takeAtRow = numRowsInCol(puzzleBoard, takeAt) - 1
    newPuzzleBoard = copy.deepcopy(puzzleBoard)
    newPuzzleBoard[takeAtRow][takeAt] = 0
    removeBlockerBlocks(newPuzzleBoard)
    switchChangerBlocks(newPuzzleBoard)
    return newPuzzleBoard


def isValidTake( takeAt, puzzleBoard, curRemoveType):
    bottomRow = getBottomRow(puzzleBoard)

    if bottomRow[takeAt] == 0 or bottomRow[takeAt] == BLOCKER_BLOCK or bottomRow[takeAt] == CHANGER_BLOCK_BLOCKING:
        return False 

    if curRemoveType == 0:
        return True
    return bottomRow[takeAt] == curRemoveType


def isPuzzleSolved( puzzleBoard ):
    #print("isSolved\n")
    #pp.pprint(puzzleBoard)
    #print("\n")
    for i in range(0, 5):
        if puzzleBoard[0][i] != 0:
            return False
    return True


def solvePuzzleOptimaly( goal, puzzleBoard, startAt, numMoves, curRemoveType, numRemoved):
    if numMoves > goal:
        return ([], "notSolved", -1)

    if isPuzzleSolved(puzzleBoard):
        return ([], "Solved", numMoves) 

    if isPuzzleDead(puzzleBoard, curRemoveType):   
        return ([], "notSolved", -1)   

    for i in range(0, 5):
        if isValidTake( i, puzzleBoard, curRemoveType):
            newRemoveType = 0 if numRemoved == 2 else getBottomRow(puzzleBoard)[i]
            newNumRemoved = 0 if numRemoved == 2 else numRemoved + 1


            newPuzzleBoard = performTake(i, puzzleBoard)
            numMovesPerformed = abs(startAt - i)

            solution, status, solvedNumMoves = solvePuzzleOptimaly(goal, newPuzzleBoard, i, numMoves + numMovesPerformed, newRemoveType, newNumRemoved)

            if status == "Solved":
                return ([i] + solution, status, solvedNumMoves)
    return ([], "notSolved", -1)


def main():
    with open('tumblePuzzle.txt', 'r') as f:
        goal = [int(x) for x in next(f).split()][0] + 1
        array = [[int(x) for x in line.split()] for line in f]

    while True :
        print("Solving with goal: {}".format(goal))
        t0= time.time()
        solution, status, numMoves = solvePuzzleOptimaly(goal, array, 2, 0, 0, 0)
        solTime = time.time() - t0
        print("Solution is {} in {} : {}".format(status, numMoves,["{} {} {}".format(solution[i * 3], solution[i * 3 + 1], solution[i * 3 + 2]) for i in range(0,len(solution)/3)]))
        print("Took: {} seconds".format(solTime))

        if status == "Solved":
            goal = numMoves - 1
        else:
            break

if __name__ == "__main__":
    main()