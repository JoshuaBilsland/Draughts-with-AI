import math
import copy
import TreeNodeClass
import QueueClass
from Constants import(
    COLOUR_ONE,
    COLOUR_TWO
)

def minimax(board, isColourOne, depthForDifficulty, alpha, beta):
    if not board.isPossibleMoves() or depthForDifficulty == 0:
        return scoreBoard(board), []

    bestMovePath = []
    if isColourOne: # Max (Colour One is black)
        bestMaxScore = -math.inf
        allLegalMovePathsList = getAllMovePaths(board, COLOUR_ONE)
        for movePath in allLegalMovePathsList:
            man = board.getMan(movePath[0][0], movePath[0][1])
            endOfTurnBoard = makeBoardDeepCopyFromMovePath(board, man, movePath)
            currentScore, ignoredReturn = minimax(endOfTurnBoard, False, depthForDifficulty-1, alpha, beta)
            if currentScore > bestMaxScore:
                bestMaxScore = currentScore
                bestMovePath = movePath
            alpha = max(alpha, bestMaxScore)
            if alpha >= beta:
                break
        return bestMaxScore, bestMovePath

    else: # Min (Colour Two is white)
        bestMinScore = math.inf
        allLegalMovePathsList = getAllMovePaths(board, COLOUR_TWO)
        for movePath in allLegalMovePathsList:
            man = board.getMan(movePath[0][0], movePath[0][1])
            endOfTurnBoard = makeBoardDeepCopyFromMovePath(board, man, movePath)
            currentScore, ignoredReturn = minimax(endOfTurnBoard, True, depthForDifficulty-1, alpha, beta)
            if currentScore < bestMinScore:
                bestMinScore = currentScore
                bestMovePath = movePath
            beta = min(beta, bestMinScore)
            if alpha >= beta:
                break
        return bestMinScore, bestMovePath




def getAllMovePaths(board, colour): # Get all possible move paths for all men/kings of the given colour
    allMovePaths = []

    allMen = board.getAllMen()
    for man in allMen:
        if man.getColour() == colour:
            allMovePaths.extend(getLegalMovesAsMovePathList(board, man))

    return allMovePaths

def makeBoardDeepCopyFromMovePath(board, man, movePath):
    boardDeepCopy = copy.deepCopy(board)
    for move in movePath:
        if len(move) != 2: # Ignore the first item in the movePath because it is the starting row and column of the man/king, not an actual move
            boardDeepCopy.makeMove(man, move)
    return boardDeepCopy

def getLegalMovesAsMovePathList(board, man): # (this is a modified version of selectMan() from Board.py) Returns a legal move tree (tree is the same as selectMan()) and a list of all root to leaf paths in the tree (which represent a all complete move/s combinations that could be made in a turn)
    moveTree = TreeNodeClass.TreeNode(man, man.getRow(), man.getColumn())
    initialMoves = board.getLegalMoves(1, man.getIsKing(), man.getRow(), man.getColumn(), man.getColour())
    queue = QueueClass.Queue(999) 

    isAlreadyKing = man.getIsKing()
    listOfMovesFound = []

    for move in initialMoves:
        moveTree.addChild(move)

    for moveChildNode in moveTree.getChildren():
        if moveChildNode.getData()[1] == True and isAlreadyKing == False:
            pass
        else:
            queue.enQueue(moveChildNode)
    
    while not queue.isEmpty():
        nextMoveToCheck = queue.deQueue()
        moveFound = nextMoveToCheck.getData()
        listOfMovesFound.append([moveFound[2],moveFound[3], moveFound[4], moveFound[5]])

        if nextMoveToCheck.getData()[6]:
            nextMoves = board.getLegalMoves((nextMoveToCheck.getData()[0]+1), nextMoveToCheck.getData()[1], nextMoveToCheck.getData()[4], nextMoveToCheck.getData()[5], man.getColour)

            for move in nextMoves:
                reversedNewAndOldRowAndColumn = [move[4],move[5],move[2],move[3]]
                if reversedNewAndOldRowAndColumn in listOfMovesFound:
                    pass
                else:
                    nextMoveToCheck.addChild(move)
        
            for moveChildNode in nextMoveToCheck.getChildren():
                moveChildNodeData = moveChildNode.getData()
                reversedNewAndOldRowAndColumn = [moveChildNodeData[4],moveChildNodeData[5],moveChildNodeData[2],moveChildNodeData[3]]
                if reversedNewAndOldRowAndColumn in listOfMovesFound:
                    pass
                elif moveChildNodeData[1] == True and isAlreadyKing == False:
                    pass
                else:
                    queue.enQueue(moveChildNode)
    
    return moveTree.getAllRootToLeafPaths(moveTree)

def scoreBoard(board): # Take a board object and score it (for the minimax algorithm)
    allManObjects = board.getAllMen() # list of all man objects left on the board
    
    numberOfColourOneMen = 0
    numberOfColourTwoMen = 0
    
    numberOfColourOneKings = 0
    numberOfColourTwoKings = 0

    for man in allManObjects:
        manColour = man.getColour
        manIsKing = man.isKing()
        if manColour == COLOUR_ONE:
            if manIsKing:
                numberOfColourOneKings += 1
            else:
                numberOfColourOneMen += 1
        else:
            if manIsKing:
                numberOfColourTwoKings += 1
            else:
                numberOfColourTwoMen += 1

    score = numberOfColourOneMen - numberOfColourTwoMen
    score += (numberOfColourOneKings - numberOfColourTwoKings)*2
    
    return score




