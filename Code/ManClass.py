import pygame
from Constants import (
    SQUARE_SIZE, 
    CROWN,
    RED
)

class Man:
    def __init__(self, row, column, colour):
        self.__row = row
        self.__column = column
        self.__colour = colour
        self.__x = self.determineX()
        self.__y = self.determineY()
        self.__isKing = False
        self.__isSelected = False


    # Get Methods
    def getRow(self):
        return self.__row

    def getColumn(self):
        return self.__column

    def getColour(self):
        return self.__colour

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y

    def getIsKing(self):
        return self.__isKing       
        

    # Set Methods
    def setIsSelected(self, boolean):
        self.__isSelected = boolean

    def setIsKing(self, boolean): # Used when a man is promoted into a king
        self.__isKing = boolean
            

    # Other Methods

    # Calculate where on the X-Axis the object is on the pygame window
    def determineX(self):
        return SQUARE_SIZE * self.__column + SQUARE_SIZE / 2


    # Calculate where on the Y-Axis the object is on the pygame window
    def determineY(self):
        return SQUARE_SIZE * self.__row + SQUARE_SIZE / 2


    # Draw the man object onto the pygame window
    def draw(self, window):
        radius = (SQUARE_SIZE / 2) - 10
        if self.__isSelected: # Draw ring to show it is currently selected -> Draw a larger circle which the man/king is then drawn over (smaller) to appear as a ring around it
            pygame.draw.circle(window, RED, (self.__x, self.__y), (radius+5))
        pygame.draw.circle(window, self.__colour, (self.__x, self.__y), radius)
        if self.__isKing: # Draw the crown image over the king to show it has been promoted from a man to a king
            window.blit(CROWN, (self.__x - CROWN.get_width()/2, self.__y - CROWN.get_height()/2))


    # Update object variables after it has been moved on the board object
    def move(self, newRow, newColumn):	
        self.__row = newRow	
        self.__column = newColumn	
        self.__x = self.determineX()	
        self.__y = self.determineY()