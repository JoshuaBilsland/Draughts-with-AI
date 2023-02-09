import math
import copy
import TreeNodeClass
import QueueClass
from Constants import(
    COLOUR_ONE,
    COLOUR_TWO
)

def minimax(board, isColourOne, depth, valueKingPromotion):
    pass

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

def getLegalMovesAsList(board, man): # Return list of boards (each representing a legal move) (this is a modified version of selectMan() from Board.py)
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
    
    moveTreeRootToNodePaths = moveTree.getRootToLeafPaths(moveTree)
    return moveTree, moveTreeRootToNodePaths


def createAllEndOfTurnBoards(board, man, moveTreeRootToNodePaths): # Take moveTreeRootToNodePaths list and create a list of deep copied boards with each full path applied
    endOfTurnBoards = []

    for path in moveTreeRootToNodePaths:
        boardDeepCopy = copy.deepcopy(board)
        deepCopyOfMan = copy.deepcopy(man)
        for move in path[-1:]: # 'path[-1:]' -> Skip the first item (root) because it is not a move
            boardDeepCopy.makeMove(deepCopyOfMan, move)
        endOfTurnBoards.append(boardDeepCopy)

    return endOfTurnBoards
