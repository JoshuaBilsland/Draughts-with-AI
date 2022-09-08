import pygame
import BoardClass
from Constants import (
    COLOUR_ONE, 
    COLOUR_TWO, 
    SQUARE_SIZE
)

class Game():
    __window = None
    __gameMode = None
    __turn = None
    __board = None
    __selectedMan = 0
    __legalMoves = []
    __slotOne = None   # turn = slot = [dbID, colour]
    __slotTwo = None
    __gameFinished = False

    def __init__(self, window, slotOne="None", slotTwo="None"):
        self.__window = window
        self.__board = BoardClass.Board()
        self.__slotOne = slotOne
        self.__slotTwo = slotTwo
        self.__turn = self.__slotOne
        
        # 1 = Playing against an AI. 2 = Playing against another player
        if self.__slotOne == None or self.__slotTwo == None:
            self.__gameMode = 2
        else:
            self.__gameMode = 1

    def updateDisplay(self): # Update the window/display
        self.__board.drawBoard(self.__window)
        pygame.display.flip()

    def getLegalMoves(self):
        return self.__legalMoves

    def getGameFinished(self):
        return self.__gameFinished
    
    def getRowAndColumnFromPos(self, pos):
        row = int(pos[1] // SQUARE_SIZE)
        column = int(pos[0] // SQUARE_SIZE)
        return row, column

    def processClick(self, pos): # Return True/False + carry out action depending on if the click is valid [Add stuff for if gameFinished == True]
        if self.__selectedMan == 0 and self.__gameFinished == False:
            rowAndColumn = self.getRowAndColumnFromPos(pos)
            validSelection = self.selectMan(rowAndColumn[0], rowAndColumn[1])
            print(self.__legalMoves)
            if validSelection == True:
                self.__board.drawLegalMoves(self.__legalMoves)
        else: # self.__selectedMan != 0 and self.__gameFinished == False
            self.__board.drawLegalMoves(self.__legalMoves)


    # To-Do:

  
    # processClick needs to select the man, check the man is the right colour, display valid moves as small blue circles
    # Tree traversal
    # Find way to work out if the player is trying to make a move
    # See selectMan point



    def selectMan(self, row, column): # Takes a row and column to check if a man exists on that square and what legal moves it can take
        self.__selectedMan = self.__board.getMan(row, column)
        if self.__selectedMan != 0 and self.__selectedMan.getColour() == self.__turn[1]: # Checks if a man exists on that square
            self.__legalMoves = self.__board.getLegalMoves(self.__selectedMan, self.__turn) # Get a list of legal moves
            newMovesFound = True
            # Use tree to find all moves + potentially combine with else to make one selectMan and avoid repeated code---------------------------------------------------------
            validSelection = True
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
        if self.__turn == COLOUR_ONE:
            self.__turn == COLOUR_TWO
        else:
            self.__turn == COLOUR_ONE

        

            