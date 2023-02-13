import pygame
import ManClass
from Constants import (
    ROWS,
    COLUMNS,
    SQUARE_SIZE, 
    COLOUR_ONE, 
    COLOUR_TWO, 
    BEIGE, 
    BROWN,
    BLUE
)


class Board:
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


    def drawBoard(self, window, legalMoves, lastMoveMade): # Draw the board squares and the men
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
        
        if legalMoves != None: # Draw circles to show possible legal moves to the user

            if lastMoveMade == None: # No moves made yet so display the moves (child nodes) of the root (starting position of the man/king)
                movesToDisplay = []
                for child in legalMoves.getChildren():
                    movesToDisplay.append(child.getData())

            
            else: # Get the children (next potential moves, if any) of the last move made
                movesToDisplay = []
                for child in lastMoveMade.getChildren():
                    movesToDisplay.append(child.getData())

            # Display circles to show where the man/king would move to (if any moves are possible)
            for move in movesToDisplay:
                radius = (SQUARE_SIZE / 2) - 30
                x = ((move[5]+1) * SQUARE_SIZE)-(SQUARE_SIZE/2) # Use newColumn to calculate X for the centre of where the circle will be
                y = ((move[4]+1) * SQUARE_SIZE)-(SQUARE_SIZE/2) # use newRow to calculate Y for the centre of where the circle will be             
                pygame.draw.circle(window, BLUE, (x, y), radius) # Draw a circle showing where the man/king could move to

                
# Get
    def getBoard(self):
        return self.__board

    def getMan(self, row, column): # Return the man object that is in the given square
        return self.__board[row][column]

    def getNumOfColourOneLeft(self):
        return self.__numOfColourOneLeft
    def getNumOfColourTwoLeft(self):
        return self.__numOfColourTwoLeft

    def getAllMen(self): # Return list of all man objects
        men = []
        for row in self.__board:
            for column in self.__board:
                if self.__board[row][column] != 0:
                    men.append(self.__board[row][column])
        return men
                    

# Other
    def makeMove(self, man, moveToMake): # Move a man object to a different position in the board list
        oldRow = moveToMake[2]
        oldColumn = moveToMake[3]
        newRow = moveToMake[4]
        newColumn = moveToMake[5]

        self.__board[newRow][newColumn] = self.__board[oldRow][oldColumn] # Move the man/king to the square it is moving to
        self.__board[oldRow][oldColumn] = 0 # Remove the man/king from the square it started on
        if moveToMake[1]: # If isKing == True, make the man into a king in case it is not one already (the move has just turned it into one), if it is already king, it will make it a king again (which won't have an impact)
            man.setIsKing(True)
        man.move(newRow, newColumn) # Update the row and column stored in the man object (which is used to determine a new y and x so the man/king can be drawn in the correct square)

        # Check if the move captures an opponent man/king (and remove it from the board/game)
        if moveToMake[6]: # If capturesMan == True
            # Work out which man/king should be captured (using the difference of the new and old rows + columns to work out which square/opponent man/king was jumped over)
            
            # Work out which direction the move moved the man/king
            if newRow > oldRow and newColumn > oldColumn: # Moved towards the bottom right/south-east
                opponentRow = (newRow - 1)
                opponentColumn = (newColumn - 1)
            elif newRow > oldRow and newColumn < oldColumn: # Move towards the bottom left/south-west
                opponentRow = (newRow - 1)
                opponentColumn = (newColumn + 1)
            elif newRow < oldRow and newColumn < oldColumn: # Moved towards the top left/north-west
                opponentRow = (newRow + 1)
                opponentColumn = (newColumn + 1)
            elif newRow < oldRow and newColumn > oldColumn: # Moved towards the top right/north-east
                opponentRow = (newRow + 1)
                opponentColumn = (newColumn - 1)
            
            # Work out man/king colour and take 1 away from variable which keeps count of the men/kings left
            if self.__board[opponentRow][opponentColumn].getColour() == COLOUR_ONE:
                self.__numOfColourOneLeft -= 1
            else:
                self.__numOfColourTwoLeft -= 1

            # Delete the man/king from the board
            self.__board[opponentRow][opponentColumn] = 0


    def wouldMakeKing(self, newRow): # Used to check if a legal move would make a man turn into a king
        boolean = False
        if newRow == 0 or newRow == (ROWS-1):
            boolean = True
        return boolean

# Getting legal moves for a man/king
    def getLegalMoves(self, moveNumber, isKing, row, column, turnColour): # moveNumber is for if a player makes multiple moves (captures) in one turn since this will change what makes a move legal (must capture again)
        legalMoves = []
    
        if turnColour == COLOUR_ONE:
            moves = self.getLegalMovesDown(moveNumber, isKing, row, column, COLOUR_TWO)
            if isKing:
                moves += self.getLegalMovesUp(moveNumber, isKing, row, column, COLOUR_TWO)
        elif turnColour == COLOUR_TWO:
            moves = self.getLegalMovesUp(moveNumber, isKing, row, column, COLOUR_ONE)
            if isKing:
                moves += self.getLegalMovesDown(moveNumber, isKing, row, column, COLOUR_ONE)
        for move in moves:
            legalMoves.append(move)
        
        # Check if any legal moves will turn the man into a king (or ignore if already is a king)
        for move in legalMoves:
            if not move[1]: # if not a king check if it will become one (if it is already king, check not needed)
                if self.wouldMakeKing(move[4]):
                    move[1] = True

        return legalMoves

    def getLegalMovesDown(self, moveNumber, isKing, row, column, oppositeManColour): # Make a list of all valid moves that could be made if the man was to move down the board
        legalMoves = []

        if moveNumber == 1: # moveNumber is used to show that these moves would be the first move that the player has made that turn (The move does not have to jump/capture a man)
            
            # Check if the square to the bottom left of the man/king is empty
            try: 
                if self.__board[row+1][column-1] == 0:
                    move = [moveNumber, isKing, row, column, row+1, column-1, False] # The list follows the structure: [moveNumber, isKing, oldRow, oldColumn, newRow, newColumn, capturesMan]. capturesMan is used to show if the move will capture a man
                    legalMoves.append(move)    
            except IndexError: # Handles the error that the square being checked doesn't exist
                pass
            
            # Check if the square to the bottom right of the man/king is empty
            try: 
                if self.__board[row+1][column+1] == 0:
                    move = [moveNumber, isKing, row, column, row+1, column+1, False]
                    legalMoves.append(move)
            except IndexError: 
                pass
    
        # Checks if a capture can be made to the left
        try: 
            square = self.__board[row+1][column-1]  # Get the contents of the square to the bottom left of the man/king
            if square != 0: # If there is a man/king in the square
                if square.getColour() == oppositeManColour: # Checks the colour of that man/king that is in that square
                    if self.__board[row+2][column-2] == 0: # Checks if there is a free square to jump to (Over the opponent's man/king)
                        move = [moveNumber, isKing, row, column, row+2, column-2, True] # True is used to show that another move could potentially be made since this move results in a capture (Multi-capture)
                        legalMoves.append(move)
        except IndexError:   
            pass
        
        # Checks if a capture can be made to the right
        try: 
            square = self.__board[row+1][column+1]
            if square != 0:
                if square.getColour() == oppositeManColour:
                    if self.__board[row+2][column+2] == 0:
                        move = [moveNumber, isKing, row, column, row+2, column+2, True]
                        legalMoves.append(move)
        except IndexError:
            pass
            
        return legalMoves

    def getLegalMovesUp(self, moveNumber, isKing, row, column, oppositeManColour): # Make a list of all valid moves that could be made if the man was to move up the board
        legalMoves = []

        if moveNumber == 1: # moveNumber is used to show that these moves would be the first move that the player has made that turn (The move does not have to jump/capture a man)
        
            # Check if the square to the top left of the man/king is empty    
            try:
                if self.__board[row-1][column-1] == 0:
                    move = [moveNumber, isKing, row, column, row-1, column-1, False] # The list follows the structure: [moveNumber, isKing, oldRow, oldColumn, newRow, newColumn, capturesMan]. capturesMan is used to show if the move will capture a man                 
                    legalMoves.append(move)
            except IndexError: # Handles the error that the square being checked doesn't exist
                pass

            # Check if the square to the top right of the man/king is empty
            try:
                if self.__board[row-1][column+1] == 0:
                    move = [moveNumber, isKing, row, column, row-1, column+1, False]
                    legalMoves.append(move)
            except IndexError:
                pass
        
        # Checks if a capture can be made to the left
        try:
            square = self.__board[row-1][column-1] # Get the contents of the square to the top left of the man/king
            if square != 0: # If there is a man/king in the square
                if square.getColour() == oppositeManColour: # Checks the colour of that man/king that is in that square
                    if self.__board[row-2][column-2] == 0: # Checks if there is a free square to jump to (Over the opponent's man/king)
                        move = [moveNumber, isKing, row, column, row-2, column-2, True] # True is used to show that another move could potentially be made since this move results in a capture (Multi-capture)
                        legalMoves.append(move)
        except IndexError:
            pass

        # Checks if a capture can be made to the right
        try:
            square = self.__board[row-1][column+1]
            if square != 0:
                if square.getColour() == oppositeManColour:
                    if self.__board[row-2][column+2] == 0:
                        move = [moveNumber, isKing, row, column, row-2, column+2, True]
                        legalMoves.append(move)
        except IndexError:
            pass
        
        return legalMoves

    def isPossibleMoves(self, colourToCheckFor): # Used to work out if a game is over or it should continue (checks for any possible legal moves, if some are found then the game could continue (depending on other factors))
        # Check for any possible moves for the colour given
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.__board[row][column] != 0:
                    if self.__board[row][column].getColour() == colourToCheckFor:
                        manToCheck = self.__board[row][column]
                        if self.getLegalMoves(1, manToCheck.getIsKing(), manToCheck.getRow(), manToCheck.getColumn(), colourToCheckFor) != []:
                            return True # A possible move was found
        return False # No possible moves

