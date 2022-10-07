import pygame
import ManClass
import Tree
from Constants import (
    ROWS,
    COLUMNS,
    SQUARE_SIZE, 
    COLOUR_ONE, 
    COLOUR_TWO, 
    BEIGE, 
    BROWN
)


class Board():
    __board = []
    __numOfColourOneLeft = 12
    __numOfColourTwoLeft = 12

    # Creates a list of where the men are which is used to then draw the board in the window
    def __init__(self):
        for row in range(ROWS):
            self.__board.append([])
            for column in range(COLUMNS):
                if row == 3 or row == 4:
                    self.__board[row].append(0)
                elif row % 2 == 0:
                    if column % 2 != 0:
                        if row < 3: # [A] Used to decide the colour of the man and stop them from being put into the middle of the board 
                            self.__board[row].append(ManClass.Man(row, column, COLOUR_ONE))
                        elif row > 4: # [A]
                            self.__board[row].append(ManClass.Man(row, column, COLOUR_TWO))
                    else:
                        self.__board[row].append(0)
                else:
                    if column % 2 == 0:
                        if row < 3: # [A]
                            self.__board[row].append(ManClass.Man(row, column, COLOUR_ONE))
                        elif row > 4: # [A]
                            self.__board[row].append(ManClass.Man(row, column, COLOUR_TWO))
                    else:
                        self.__board[row].append(0)


    # Other
    def drawBoard(self, window): # Draw the board squares and the men
        # Draw board pattern
        for row in range(ROWS):
            for column in range(COLUMNS):
                if row % 2 == 0:    # Changes pattern based on the row
                    if column % 2 == 0:
                        pygame.draw.rect(window, BEIGE, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        pygame.draw.rect(window, BROWN, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    if column % 2 == 0:
                        pygame.draw.rect(window, BROWN, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        pygame.draw.rect(window, BEIGE, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        # Draw men onto the board
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.__board[row][column] != 0:
                    self.__board[row][column].draw(window)
        
        #self.drawLegalMoves(legalMoves) # Draw the legal moves onto the board

    def getBoard(self):
        return self.__board

    def getMan(self, row, column): # Return the man object that is in the given square
        return self.__board[row][column]

    def getAllMenCoordinates(self, colourToGet): # Return a list of all the coordinates of all the men of a certain colour, that are on the board
        coordinates = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.board[row][column] != 0: # Check the square is not empty
                    if self.__board[row][column].getColour() == colourToGet: # Check that the man/king is the same colour that is being searched for
                        coordinates.append([row, column])
        return coordinates

    def moveMan(self, man, newRow, newColumn): # Move a man object to a different position in the board list
        oldRow = man.getRow()
        oldColumn = man.getColumn()
        self.__board[oldRow][oldColumn], self.__board[newRow][newColumn] = self.__board[newRow][newColumn], self.__board[oldRow][oldColumn] # Swaps the values of the old and new square
        man.move(newRow, newColumn) # Update the row and column class variables of the man object that has been moved

        if newRow == 0 or newRow == (ROWS-1): # If the man gets to the other side of the board, make it a king
            man.makeKing() 

    def drawLegalMoves(self, legalMoves): # Draw circles to show the player what legal moves they can make ---------------------------------------------------------------------------------------------------
        print()

    def getLegalMoves(self, man, moveNumber, slot): # moveNumber is for if a player makes multiple moves (captures) in one turn since this will change what makes a move legal (must capture again)
        legalMoves = []
        if slot != None: # If it is a real player's turn 
            if slot[1] == COLOUR_ONE: # Determines which colour the man/king can take (Opposite colour to the player)
                temp = self.getLegalMovesDown(COLOUR_TWO, moveNumber, man.getRow(), man.getColumn())
                for move in temp:
                    legalMoves.append(move) 
            else: # If they are COLOUR_TWO
                temp = self.getLegalMovesUp(COLOUR_ONE, moveNumber, man.getRow(), man.getColumn())
                for move in temp:
                    legalMoves.append(move) 
        
        else: # If it is an AI's turn
            coordinates = self.getAllMenCoordinates()

        return legalMoves

    def getLegalMovesDown(self, oppositeManColour, moveNumber, row, column): # Make a list of all valid moves that could be made if the man was to move down the board
        legalMoves = []

        if moveNumber == 1: # moveNumber is used to show that these moves would be the first move that the player has made that turn (The move does not have to jump/capture a man)
            
            # Check if the square to the bottom left of the man/king is empty
            try: 
                if self.__board[row+1][column-1] == 0:
                    move = [moveNumber, row, column, row+1, column-1, False] # The list follows the structure: [moveNumber, oldRow, oldColumn, newRow, newColumn, capturesMan]. capturesMan is used to show if the move will capture a man
                    legalMoves.append(move)    
            except IndexError: # Handles the error that the square being checked doesn't exist
                pass
            
            # Check if the square to the bottom right of the man/king is empty
            try: 
                if self.__board[row+1][column+1] == 0:
                    move = [moveNumber, row, column, row+1, column+1, False]
                    legalMoves.append(move)
            except IndexError: 
                pass
    
        # Checks if a capture can be made to the left
        try: 
            square = self.__board[row+1][column-1]  # Get the contents of the square to the bottom left of the man/king
            if square != 0: # If there is a man/king in the square
                if square.getColour() == oppositeManColour: # Checks the colour of that man/king that is in that square
                    if self.__board[row+2][column-2] == 0: # Checks if there is a free square to jump to (Over the opponent's man/king)
                        move = [moveNumber, row, column, row+2, column-2, True] # True is used to show that another move could potentially be made since this move results in a capture (Multi-capture)
                        legalMoves.append(move)
        except IndexError:   
            pass
        
        # Checks if a capture can be made to the right
        try: 
            square = self.__board[row+1][column+1]
            if square != 0:
                if square.getColour() == oppositeManColour:
                    if self.__board[row+2][column+2] == 0:
                        move = [moveNumber, row, column, row+2, column+2, True]
                        legalMoves.append(move)
        except IndexError:
            pass
            
        return legalMoves

    def getLegalMovesUp(self, oppositeManColour, moveNumber, row, column): # Make a list of all valid moves that could be made if the man was to move up the board
        legalMoves = []

        if moveNumber == 0: # moveNumber is used to show that these moves would be the first move that the player has made that turn (The move does not have to jump/capture a man)
        
            # Check if the square to the top left of the man/king is empty    
            try:
                if self.__board[row-1][column-1] == 0:
                    move = [moveNumber, row, column, row-1, column-1, False] # The list follows the structure: [moveNumber, oldRow, oldColumn, newRow, newColumn, capturesMan]. capturesMan is used to show if the move will capture a man                 
                    legalMoves.append(move)
            except IndexError: # Handles the error that the square being checked doesn't exist
                pass

            # Check if the square to the top right of the man/king is empty
            try:
                if self.__board[row-1][column+1] == 0:
                    move = [moveNumber, row, column, row-1, column+1, False]
                    legalMoves.append(move)
            except IndexError:
                pass
        
        # Checks if a capture can be made to the left
        try:
            square = self.__board[row-1][column-1] # Get the contents of the square to the top left of the man/king
            if square != 0: # If there is a man/king in the square
                if square.getColour() == oppositeManColour: # Checks the colour of that man/king that is in that square
                    if self.__board[row-2][column-2] == 0: # Checks if there is a free square to jump to (Over the opponent's man/king)
                        move = [moveNumber, row, column, row-1, column+1, True] # True is used to show that another move could potentially be made since this move results in a capture (Multi-capture)
                        legalMoves.append(move)
        except IndexError:
            pass

        # Checks if a capture can be made to the right
        try:
            square = self.__board[row-1][column+1]
            if square != 0:
                if square.getColour() == oppositeManColour:
                    if self.__board[row-2][column+2] == 0:
                        move = [moveNumber, row, column, row-1, column+1, True]
                        legalMoves.append(move)
        except IndexError:
            pass
        
        return legalMoves

     

