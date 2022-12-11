import pygame
import BoardClass
import TreeClass
from Constants import (
    COLOUR_ONE, 
    COLOUR_TWO, 
    SQUARE_SIZE
)

class Game:
    def __init__(self, window, chosenGameMode, chosenColour, slotOne=None, slotTwo=None, AIDifficulty=None):
        self.__window = window
        self.__gameMode = chosenGameMode
        self.__board = BoardClass.Board()
        self.__selectedMan = None 
        self.__legalMoves = []
        self.__slotOne = slotOne # None is used if the slot is not being used (for example, PvAI will have only one slot being used)
        self.__slotTwo = slotTwo
        self.__gameFinished = False
        self.__AIDifficulty = AIDifficulty # None is used if the game mode is PvP and not PvAI (since in PvP they AI isn't used)
        
        # Determine who should go first (whose turn)
        if self.__gameMode == "PvP":
            if chosenColour == COLOUR_ONE:
                self.__turn = self.__slotOne, COLOUR_ONE # colour one (black) chosen for slot one to play as, black/slotOne goes first
            else:
                self.__turn = self.__slotTwo, COLOUR_ONE # colour two (white) chosen for slot one to play as, black given to slot two and so slotTwo goes first
        else: # gameMode == "PvAI"
            if self.__slotOne != None: # slot one was passed, means that slot one was chosen for the player to play as against the AI (slotTwo will not be passed, None will be passed instead to show it is not being used)
                if chosenColour == COLOUR_ONE:
                    self.__turn = self.__slotOne, COLOUR_ONE # colour one (black) chosen for slot one to play as, black/slotOne goes first
                else:
                    self.__turn = "AI", COLOUR_ONE  # colour two (white) was chosen for slot one to play as, black given to the AI. Black/AI will go first
            else: # slot two was passed, means that slot two was chosen for the player to play as against the AI (slotOne will not be passed, None will be passed instead to show it is not being used)
                if chosenColour == COLOUR_ONE:
                    self.__turn = self.__slotTwo, COLOUR_ONE
                else:
                    self.__turn = "AI", COLOUR_ONE        


    # Get
    def getLegalMoves(self):
        return self.__legalMoves
    
    def getRowAndColumnFromPos(self, pos):
        row = int(pos[1] // SQUARE_SIZE)
        column = int(pos[0] // SQUARE_SIZE)
        return row, column

    def getGameFinished(self):
        return self.__gameFinished


    # Other
    def updateDisplay(self): # Update the window/display
        self.__board.drawBoard(self.__window)
        pygame.display.flip()
    
    def processClick(self, mousePos): # Return True/False + carry out action depending on if the click is valid [Add stuff for if gameFinished == True]
        rowAndColumn = self.getRowAndColumnFromPos(mousePos)
        if self.__selectedMan == None: # if no man is selected, check the user clicked a man and then select it (and get its legal moves)
            if self.__board.getMan(rowAndColumn[0], rowAndColumn[1]) != 0: # check the user clicked a square that has a man in it (it is not empty)
                self.selectMan(rowAndColumn[0], rowAndColumn[1])

    def selectMan(self, row, column): # Takes a row and column to check if a man exists on that square and what legal moves it can take
        self.__selectedMan = self.__board.getMan(row, column)
        if self.__selectedMan != 0:  # Checks if a man exists on that square (0 means that it is an empty square)
            if self.__selectedMan.getColour() == self.__turn[1]: # Check the selected man is the colour of whose turn it is
                self.__legalMoves = TreeClass.TreeNode([self.__selectedMan.getRow(), self.__selectedMan.getColumn()]) # Tree nodes store legal moves, root is the starting row and column of the selected man
                initialMoves = self.__board.getLegalMoves(self.__selectedMan, self.__selectedMan.getRow(), self.__selectedMan.getColumn, 1, self.__turn[1]) # Moves that can be made from where the man currently is (opening moves)
                # Add the moves as children of the root (man starting position)
                for move in initialMoves:
                    self.__legalMoves.addChild(move)

                # Get moves that can be made after the opening moves (if any), and then moves after those moves (if any), and so on

                
        else:
            self.__legalMoves = []
            validSelection = False
            self.__selectedMan = 0
        
        return validSelection # Return if the selection was valid (was there a man in the give square on the board)
        
    def moveMan(self, newRow, newColumn): # Move a man to a new square
        if self.__selectedMan != 0 and (newRow, newColumn) in self.__legalMoves:
            self.__board.moveMan(self.__selectedMan, newRow, newColumn)
    
    def AIMove(self): # Used to carry out an AI's move (get legal moves, work out best move, make move)
        print("temp----------------------------------------")


    def endTurn(self):
        # Change slot/player/ai
        if self.__gameMode == "PvP":
            if self.__turn[0] == self.__slotOne: # slotOne -> slotTwo
                self.__turn[0] = self.__slotTwo
            else: # slotTwo -> slotOne
                self.__turn[0] = self.__slotOne

        else: # gameMode == "PvAI"
            if self.__turn[0] == self.__slotOne or self.__turn[0] == self.__slotTwo:
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
        if self.__turn[0] == "AI":
            self.AIMove()         

            