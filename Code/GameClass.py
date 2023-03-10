import pygame
import BoardClass
import TreeNodeClass
import QueueClass
import Minimax
import math
import copy
from Constants import (
    COLOUR_ONE, 
    COLOUR_TWO, 
    SQUARE_SIZE,
    ROWS,
    COLUMNS
)

class Game:
    def __init__(self, window, chosenGameMode, chosenColour, slotOne=None, slotTwo=None, AIDifficulty=None):
        self.__window = window
        self.__gameMode = chosenGameMode
        self.__chosenColour = chosenColour
        self.__board = BoardClass.Board()
        self.__selectedMan = None 
        self.__legalMoves = None
        self.__lastMoveMade = None # Used to work out which possible move locations to display next + to work out if a user should be able to change the man/king they have selected (if they have made a move they should not be able to move another man/king)
        self.__slotOne = slotOne # None is used if the slot is not being used (for example, PvAI will have only one slot being used)
        self.__slotTwo = slotTwo
        self.__slotOneTotalNumberOfMoves = 0 # Track how many moves each has made in the current game 
        self.__slotTwoTotalNumberOfMoves = 0
        self.__gameFinished = False
        self.__winner = None
        self.__AIDifficulty = AIDifficulty # None is used if the game mode is PvP and not PvAI (since in PvP they AI isn't used)
        
        # Determine who should go first (whose turn)
        if self.__gameMode == "PvP":
            if self.__chosenColour == COLOUR_ONE:
                self.__turn = [self.__slotOne, COLOUR_ONE] # colour one (black) chosen for slot one to play as, black/slotOne goes first
            else:
                self.__turn = [self.__slotTwo, COLOUR_ONE] # colour two (white) chosen for slot one to play as, black given to slot two and so slotTwo goes first
        else: # gameMode == "PvAI"
            if self.__slotOne != None: # slot one was passed, means that slot one was chosen for the player to play as against the AI (slotTwo will not be passed, None will be passed instead to show it is not being used)
                if self.__chosenColour == COLOUR_ONE:
                    self.__turn = [self.__slotOne, COLOUR_ONE] # colour one (black) chosen for slot one to play as, black/slotOne goes first
                else:
                    self.__turn = ["AI", COLOUR_ONE]  # colour two (white) was chosen for slot one to play as, black given to the AI. Black/AI will go first
            else: # slot two was passed, means that slot two was chosen for the player to play as against the AI (slotOne will not be passed, None will be passed instead to show it is not being used)
                if self.__chosenColour == COLOUR_ONE:
                    self.__turn = [self.__slotTwo, COLOUR_ONE]
                else:
                    self.__turn = ["AI", COLOUR_ONE]        


    # Get
    def getLegalMoves(self):
        return self.__legalMoves
    
    def getRowAndColumnFromPos(self, pos):
        row = int(pos[1] // SQUARE_SIZE)
        column = int(pos[0] // SQUARE_SIZE)
        return row, column

    def getGameFinished(self):
        return self.__gameFinished

    def getWinner(self):
        return self.__winner

    def getSlotOneTotalNumberOfMoves(self):
        return self.__slotOneTotalNumberOfMoves
    
    def getSlotOneTotalNumberOfMoves(self):
        return self.__slotTwoTotalNumberOfMoves

    # Other
    def updateDisplay(self): # Update the window/display
        self.__board.drawBoard(self.__window, self.__legalMoves, self.__lastMoveMade)
        pygame.display.flip()
    
    def processClick(self, mousePos): # Return True/False + carry out action depending on if the click is valid [Add stuff for if gameFinished == True]
        rowAndColumn = self.getRowAndColumnFromPos(mousePos)
        if self.__selectedMan == None: # if no man is selected, check the user clicked a man and then select it (and get its legal moves)
            # Checks if a man exists on that square (0 means that it is an empty square) + the man belongs to the person whose turn it is + the user should not be able to select a different man/king if they have already moved one this turn
            if self.__board.getMan(rowAndColumn[0], rowAndColumn[1]) != 0 and self.__board.getMan(rowAndColumn[0], rowAndColumn[1]).getColour() == self.__turn[1] and self.__lastMoveMade == None: 
                self.selectMan(rowAndColumn[0], rowAndColumn[1])
                self.__selectedMan.setIsSelected(True)
        
        elif self.__selectedMan != None: # If a man/king is already selected
            if self.__board.getMan(rowAndColumn[0], rowAndColumn[1]) != 0 and self.__board.getMan(rowAndColumn[0], rowAndColumn[1]).getColour() == self.__turn[1] and self.__lastMoveMade == None: # Unselect the currently selected man, reset required variables, select the new man
                self.__selectedMan.setIsSelected(False)
                self.__legalMoves = None
                self.__lastMoveMade = None
                self.selectMan(rowAndColumn[0], rowAndColumn[1])
                self.__selectedMan.setIsSelected(True)

            elif self.__board.getMan(rowAndColumn[0], rowAndColumn[1]) == 0: # If the user clicks an empty square, work out if the selected man should be unselected or if a move should be made (check if the square is a destination of a legal move)
                if self.__lastMoveMade == None: # If lastMoveMade is None, get the children (legal moves) from the root node (starting position) and check those moves (to see if the square the user clicked is where the man/king will move to if that move is made)
                    movesToCheck = []
                    for child in self.__legalMoves.getChildren():
                        movesToCheck.append(child.getData())
                    
                else: # The user has made a move and so check the children (next legal moves) of that move and check those moves (to see if the square the user clicked is where the man/king will move to if that move is made)
                    movesToCheck = []
                    for child in self.__lastMoveMade.getChildren():
                        movesToCheck.append(child.getData())
                
                isDestination = False # Tracks if where the user clicked is a destination of a legal move (if it is, the move will be made, otherwise the selected man/king will be unselected (unless they have made a move already with it this turn))
                for move in movesToCheck:
                    moveNewRowToCheck = move[4]
                    moveNewColumnToCheck = move[5]
                    if moveNewRowToCheck == rowAndColumn[0] and moveNewColumnToCheck == rowAndColumn[1]:
                        isDestination = True
                        moveToMake = move
                
                # Carry out the move OR unselect the man OR do nothing
                if isDestination: # Carry out the move
                    self.__board.makeMove(self.__selectedMan, moveToMake)
                    
                    # Get move object
                    if self.__lastMoveMade == None:
                        for node in self.__legalMoves.getChildren():
                            if node.getData() == moveToMake:
                                self.__lastMoveMade = node
                    else:
                        for node in self.__lastMoveMade.getChildren():
                            if node.getData() == moveToMake:
                                self.__lastMoveMade = node

                    if self.__lastMoveMade.getChildren() == []: # End turn if the player cannot make any more moves this turn
                        self.endTurn()
                
                elif not isDestination and self.__lastMoveMade == None: # The user has not made a move with the selected man/king yet so allow them to unselect it by clicking an empty square (unselect the man)
                    self.__legalMoves = None
                    self.__lastMoveMade = None
                    self.__selectedMan.setIsSelected(False)

    def selectMan(self, row, column): # Takes a row and column to check if a man exists on that square and what legal moves it can take
        self.__selectedMan = self.__board.getMan(row, column)
        self.__legalMoves = TreeNodeClass.TreeNode([self.__selectedMan.getRow(), self.__selectedMan.getColumn()]) # Tree nodes store legal moves, root is the starting row and column of the selected man
        initialMoves = self.__board.getLegalMoves(1, self.__selectedMan.getIsKing(), self.__selectedMan.getRow(), self.__selectedMan.getColumn(), self.__turn[1]) # Moves that can be made from where the man currently is (opening moves)
        queue = QueueClass.Queue(999) # Queue used for breadth-first traversal of the tree of possible moves
        
        isAlreadyKing = self.__selectedMan.getIsKing() # Used to check if the turn has just promoted the man to a king and therefore the turn should end (and any move after that should not be checked/checked for)
        listOfMovesFound = [] # Used to make sure turn ends when a man is promoted to a king

        # Add the moves as children of the root (man starting position)
        for move in initialMoves:
            self.__legalMoves.addChild(move)

        # Add the moves (now children nodes) into the queue (to check if further moves could be made via multi-capturing opponents men)
        for moveChildNode in self.__legalMoves.getChildren():
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
                nextMoves = self.__board.getLegalMoves((nextMoveToCheck.getData()[0]+1), nextMoveToCheck.getData()[1], nextMoveToCheck.getData()[4], nextMoveToCheck.getData()[5], self.__turn[1])

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


    def AIMove(self): # Used to carry out an AI's move (get legal moves, work out best move, make move)
        if self.__AIDifficulty == 1: # Easy
            depthForDifficulty = 2
        elif self.__AIDifficulty == 2: # Average
            depthForDifficulty = 4
        elif self.__AIDifficulty == 3: # Hard
            depthForDifficulty = 6
        elif self.__AIDifficulty == 4: # Expert 
            depthForDifficulty = 8

        if self.__turn[1] == COLOUR_ONE:
            bestMovePath = Minimax.minimax(self.__board, True, depthForDifficulty, -math.inf, math.inf)
        else:
            bestMovePath = Minimax.minimax(self.__board, False, depthForDifficulty, -math.inf, math.inf)

        self.__board = bestMovePath[1]
        self.endTurn()


    def endTurn(self):        
        # Check if game is finished (someone has won or there is a draw)
        checkResults = self.workOutIsGameFinished(self.__turn[1])
        self.__gameFinished = checkResults[0]
        
        if self.__gameFinished:
            # Work out if a slot (and which one) or the AI won
            if checkResults[1] == None:
                self.__winner = None # Game ends but it was a draw so no winner
            elif self.__gameMode == "PvP":
                if checkResults[1] == self.__chosenColour:
                    self.__winner = "S1" # slot one
                else:
                    self.__winner = "S2" # slot two
            elif self.__gameMode == "PvAI": # gameMode == "PvAI"
                if self.__slotOne != None: # Slot one was passed to be used against the AI
                    if checkResults[1] == self.__chosenColour: # The colour that won is the won that slot one chose, means slotOne won
                        self.__winner = "S1"
                    else:
                        self.__winner = "AI" # The colour that won was the one used by the AI (since the user did not choose to play as it), AI won
                else: # Slot one was not passed so slot two must be being used
                    if checkResults[1] == self.__chosenColour:
                        self.__winner = "S2"
                    else:
                        self.__winner = "AI"

        # Wipe selectedMan,legalMoves,lastMoveMade -> the AI does not use these so they do not need to be wiped
        if not self.__turn[0] == "AI":
            self.__selectedMan.setIsSelected(False)        
            self.__selectedMan = None
            self.__legalMoves = None
            self.__lastMoveMade = None

        # Change slot/player/ai
        if self.__gameMode == "PvP":
            if self.__turn[0] == self.__slotOne: # slotOne -> slotTwo
                self.__slotOneTotalNumberOfMoves += 1
                self.__turn[0] = self.__slotTwo
            else: # slotTwo -> slotOne
                self.__slotTwoTotalNumberOfMoves += 1
                self.__turn[0] = self.__slotOne

        else: # gameMode == "PvAI"
            if self.__turn[0] == self.__slotOne or self.__turn[0] == self.__slotTwo:
                if self.__slotOne != None: # Slot one chosen
                    self.__slotOneTotalNumberOfMoves += 1
                else: # Slot two chosen
                    self.__slotTwoTotalNumberOfMoves += 1
                self.__turn[0] = "AI" # AI's Turn
            else: # == "AI"
                # Check which slot is being used
                if self.__slotOne != None:
                    # slot one is being used
                    self.__turn[0] = self.__slotOne # AI -> slotOne
                else:
                    # slotTwo is being used
                    self.__turn[0] = self.__slotTwo # AI -> slotTwo

        # Change colour
        if self.__turn[1] == COLOUR_ONE: # colourOne -> colourTwo
            self.__turn[1] = COLOUR_TWO
        else: # colourTwo -> colourOne
            self.__turn[1] = COLOUR_ONE

        # Carry out AI turn (if needed)
        if self.__turn[0] == "AI" and self.__gameFinished == False:
            self.AIMove()

        print("S1Moves",self.__slotOneTotalNumberOfMoves)
        print("S2Moves",self.__slotTwoTotalNumberOfMoves)

    def workOutIsGameFinished(self, turnColour):
        returnSet = []

        # Check if side have had all their men/kings captured (the other side has won)
        if self.__board.getNumOfColourOneLeft == 0:
            returnSet.extend([True, COLOUR_TWO]) # Structure -> [isGameFinished, whoWon]
        elif self.__board.getNumOfColourTwoLeft == 0:
            returnSet.extend([True, COLOUR_ONE])
        else:
            # Check if their is a draw (check if no more moves are possible)
            colourOneMovesPossible = self.__board.isPossibleMoves(COLOUR_ONE) # Store if any moves are possible for colour one
            colourTwoMovesPossible = self.__board.isPossibleMoves(COLOUR_TWO)

            if colourOneMovesPossible == False and colourTwoMovesPossible == False:
                returnSet.extend([True, None]) # It is a draw since there are no more legal moves

            elif colourOneMovesPossible == True and colourTwoMovesPossible != True:
                returnSet.extend([True, COLOUR_ONE]) # Colour one has one since colour two cannot make any more moves
            
            elif colourOneMovesPossible != True and colourTwoMovesPossible == True:
                returnSet.extend([True, COLOUR_TWO]) # Colour two has one since colour one cannot make any more moves

            else:
                returnSet.extend([False, None]) # Game is not finished -> there are still men/kings left and possible legal moves for at least one of them
        return returnSet
    
    def workOutIsGameFinished(self, turnColour):
        returnSet = []

        if turnColour == COLOUR_ONE: # COlOUR_ONE has just made a move so check COLOUR_TWO before switching turn (as the game might already be over)
            # next turn will be COLOUR_TWO so check if COLOUR_TWO has any moves left
            if self.__board.getNumOfColourTwoLeft == 0:
                returnSet.extend([True, COLOUR_ONE]) # Structure -> [isGameFinished, whoWon]
                
        else: # COlOUR_TWO has just made a move so check COLOUR_ONE before switching turn (as the game might already be over)
            # next turn will be COLOUR_ONE so check if COLOUR_ONE has any moves left
            if self.__board.getNumOfColourOneLeft == 0:
                returnSet.extend([True, COLOUR_TWO])

        colourOneMovesPossible = self.__board.isPossibleMoves(COLOUR_ONE) # Store if any moves are possible for colour one (boolean)
        colourTwoMovesPossible = self.__board.isPossibleMoves(COLOUR_TWO) # colour two as well
            
        if colourOneMovesPossible == False and colourTwoMovesPossible == False:
            returnSet.extend([True, None]) # It is a draw since there are no more legal moves, regardless of whose turn it was and will be

        elif colourOneMovesPossible == True and colourTwoMovesPossible == False and turnColour == COLOUR_ONE:
            returnSet.extend([True, COLOUR_ONE]) # Colour one has won since colour two cannot make any more moves when the turn switches to theirs
         
        elif colourOneMovesPossible == False and colourTwoMovesPossible == True and turnColour == COLOUR_TWO:
            returnSet.extend([True, COLOUR_TWO]) # Colour two has won since colour one cannot make any more moves when the turn switches to theirs

        elif len(returnSet) == 0: # No previous condition was met (and so returnSet was not changed) so the game is not finished
            returnSet.extend([False, None]) # Game is not finished -> there are still men/kings left and possible legal moves for at least one of them
        
        return returnSet       