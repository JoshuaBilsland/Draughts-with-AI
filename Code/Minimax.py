import math
import copy
import TreeNodeClass
import QueueClass
from Constants import(
    COLOUR_ONE,
    COLOUR_TWO
)

# Used by the AI to decide what is the best possible move to make for a given board and colour
def minimax(board, isColourOne, depthForDifficulty, alpha, beta):
    if isColourOne:
        turnColour = COLOUR_ONE
    else:
        turnColour = COLOUR_TWO
    if board.workOutIsGameFinished(turnColour)[0] or depthForDifficulty == 0: # Base case: The game is over or the it has reached the depth limit (starts at a number and each call takes away 1 until it hits 0)
        return scoreBoard(board), board
    
    if isColourOne: # Max (Colour One is black)
        bestBoard = None # The board after the best move path has been applied to it
        bestMaxScore = -math.inf # -inf is used so that any score (and board) is better
        allMovePaths = getAllMovePaths(board, COLOUR_ONE) # Get all root-to-leaf move paths for a given board and colour
        if len(allMovePaths) == 0: # Return score and board since no valid moves exist
            return scoreBoard(board), board
        allDeepCopiedBoards = makeAllDeepCopiedBoards(board, allMovePaths) # For each move path, make a deepcopy board with that move path applied
        for deepCopiedBoard in allDeepCopiedBoards:
            currentScore, ignoredBoardDuplicate = minimax(deepCopiedBoard, False, depthForDifficulty-1, alpha, beta) # Call minimax on the deepcopy boards
            if currentScore > bestMaxScore: # Compare the score to see if the deepcopy board is a better outcome than the previous best
                bestMaxScore = currentScore
                bestBoard = deepCopiedBoard
            # Alpha-beta pruning to make minimax more efficient and faster to produce a result (reduces the number of boards/branches that need to be checked)
            alpha = max(alpha, bestMaxScore)
            if alpha >= beta:
                break
        return bestMaxScore, bestBoard

    else: # Min (Colour Two is white)
        bestBoard = None # The board after the best move path has been applied to it
        bestMinScore = math.inf # inf is used so that any score (and board) is better
        allMovePaths = getAllMovePaths(board, COLOUR_TWO) # Get all root-to-leaf move paths for a given board and colour
        if len(allMovePaths) == 0: # Return score and board since no valid moves exist
            return scoreBoard(board), board
        allDeepCopiedBoards = makeAllDeepCopiedBoards(board, allMovePaths) # For each move path, make a deepcopy board with that move path applied
        for deepCopiedBoard in allDeepCopiedBoards:
            currentScore, ignoredBoardDuplicate = minimax(deepCopiedBoard, True, depthForDifficulty-1, alpha, beta) # Call minimax on the deepcopy boards
            if currentScore < bestMinScore: # Compare the score to see if the deepcopy board is a better outcome than the previous best
                bestMinScore = currentScore
                bestBoard = deepCopiedBoard
            # Alpha-beta pruning to make minimax more efficient and faster to produce a result (reduces the number of boards/branches that need to be checked)
            beta = min(beta, bestMinScore)
            if alpha >= beta:
                break
        return bestMinScore, bestBoard
    

# For every move path, call deepCopyBoardAndApplyMovePath(), append the returned deepcopy board to a list, return the list of deepcopied boards
def makeAllDeepCopiedBoards(board, allMovePaths):
    allDeepCopiedBoards = []
    for movePathCollection in allMovePaths: # allMovePath is a 4D list so needs to go two levels down
        for movePath in movePathCollection:
            boardDeepCopy = deepCopyBoardAndApplyMovePath(board, movePath)
            allDeepCopiedBoards.append(boardDeepCopy)
    return allDeepCopiedBoards


# Take a board, deepcopy it, apply a movePath to the deepcopy, return the deepcopy
def deepCopyBoardAndApplyMovePath(board, movePath): 
    deepCopiedBoard = copy.deepcopy(board)
    for move in movePath:
        if len(move) != 2:
            currentRow = move[2]
            currentColumn = move[3]
            man = deepCopiedBoard.getMan(currentRow, currentColumn)
            deepCopiedBoard.makeMove(man, move)
    return deepCopiedBoard


# Get all move paths for a given colour on a given board (every possible move and combination of captures)
def getAllMovePaths(board, colourToGet):
    allMovePaths = []

    menToCheck = []
    allMen = board.getAllMen()
    for man in allMen:
        if man.getColour() == colourToGet:
            allMovePaths.append(getLegalMovesAsMovePathList(board, man.getRow(), man.getColumn()))


    # Go through the list of move paths and remove any list (path) which only has one item (a move path that does not actually move any man/king)
    updatedAllMovePaths = []
    for movePathCollection in allMovePaths:
        appendCollection = False
        for movePath in movePathCollection:
            if len(movePath) != 1:
                appendCollection = True
        if appendCollection == True:
            updatedAllMovePaths.append(movePathCollection)
    return updatedAllMovePaths


# get all the legal moves (as a 4D list of root-to-leaf paths) for the man/king in a given row and column -> this code is a modified version of the selectMan() method of the 'Game' class
def getLegalMovesAsMovePathList(board, row, column): # Takes a row and column to check if a man exists on that square and what legal moves it can take
    man = board.getMan(row, column)
    legalMoves = TreeNodeClass.TreeNode([man.getRow(), man.getColumn()]) # Tree nodes store legal moves, root is the starting row and column of the selected man
    initialMoves = board.getLegalMoves(1, man.getIsKing(), man.getRow(), man.getColumn(), man.getColour()) # Moves that can be made from where the man currently is (opening moves)
    queue = QueueClass.Queue(999) # Queue used for breadth-first traversal of the tree of possible moves
    
    isAlreadyKing = man.getIsKing() # Used to check if the turn has just promoted the man to a king and therefore the turn should end (and any move after that should not be checked/checked for)
    listOfMovesFound = [] # Used to make sure turn ends when a man is promoted to a king

    # Add the moves as children of the root (man starting position)
    for move in initialMoves:
        legalMoves.addChild(move)

    # Add the moves (now children nodes) into the queue (to check if further moves could be made via multi-capturing opponents men)
    for moveChildNode in legalMoves.getChildren():
        if moveChildNode.getData()[1] == True and isAlreadyKing == False:
            # This move would promote the man to a king and so no further moves should be made (so don't enqueue to look for further moves)
            pass
        else:
            queue.enQueue(moveChildNode)
        
    # Get moves that can be made after the opening moves (if any), and then moves after those moves (if any), and so on (via tree, queue, and breadth-first traversal)
    # -> the idea being that each level down the tree represents the next move that could be made that turn (multiple moves made via multi-captures of opponents men/kings)

    while not queue.isEmpty():
        nextMoveToCheck = queue.deQueue() # Get the next move from the queue, extract the newRow and newColumn (new position) and check if any moves can be made after this move (multi-captures)
        moveFound = nextMoveToCheck.getData()
        listOfMovesFound.append([moveFound[2],moveFound[3], moveFound[4], moveFound[5]])

        if nextMoveToCheck.getData()[6]: # if capturesMan == True -> only check the mov/pos if it resulted in a piece being captured. Another move will only be possible if the previous captured a piece
            nextMoves = board.getLegalMoves((nextMoveToCheck.getData()[0]+1), nextMoveToCheck.getData()[1], nextMoveToCheck.getData()[4], nextMoveToCheck.getData()[5], man.getColour())

            for move in nextMoves: # add new moves as child nodes of the previous move
                reversedNewAndOldRowAndColumn = [move[4],move[5],move[2],move[3]] # Reverses the old and new row and column to check if the moves discovered is just going back over a piece that WOULD have been taken (see below)
                if reversedNewAndOldRowAndColumn in listOfMovesFound: # Stops the king being able to go back and forth over the same piece (it will keep finding the legal moves to do this since while it is finding legal moves, none of the opponents man/king will actually be removed from the board. This means it will jump over a man/king and then discover the move to go back over it.) 
                    pass
                else:
                    nextMoveToCheck.addChild(move)
            
            for moveChildNode in nextMoveToCheck.getChildren(): # add the moves to the queue (to check if any further moves could be made after any of them -> via breadth-first traversal)
                moveChildNodeData = moveChildNode.getData()
                reversedNewAndOldRowAndColumn = [moveChildNodeData[4],moveChildNodeData[5],moveChildNodeData[2],moveChildNodeData[3]]
                if reversedNewAndOldRowAndColumn in listOfMovesFound:
                    pass
                elif moveChildNodeData[1] == True and isAlreadyKing == False:
                    # This move would promote the man to a king and so no further moves should be made (so don't enqueue to look for further moves)
                    pass
                else:
                    queue.enQueue(moveChildNode)
    
    return legalMoves.getAllRootToLeafPaths(legalMoves) # Traverse the tree to get a 2D list of all root to leaf paths 


# Take a board object and score it (for the minimax algorithm)
def scoreBoard(board): 
    allManObjects = board.getAllMen() # list of all man objects left on the board
    
    numberOfColourOneMen = 0
    numberOfColourTwoMen = 0
    
    numberOfColourOneKings = 0
    numberOfColourTwoKings = 0

    for man in allManObjects:
        manColour = man.getColour()
        manIsKing = man.getIsKing()
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

    colourOneScore = numberOfColourOneMen + (numberOfColourOneKings)*1.5
    colourTwoScore = numberOfColourTwoMen + (numberOfColourTwoKings)*1.5
    
    return colourOneScore - colourTwoScore