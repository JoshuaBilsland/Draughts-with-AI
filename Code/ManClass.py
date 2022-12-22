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


    # Get
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
        

    # Set 
    def setIsSelected(self, boolean):
        self.__isSelected = boolean

    def setIsKing(self, boolean): # Used when a man is promoted into a king
        self.__isKing = boolean
        self.draw() # Redrawing the man/king will now also draw the crown since isKing is True
            

    # Other
    def determineX(self):
        x = SQUARE_SIZE * self.__column + SQUARE_SIZE / 2
        return x

    def determineY(self):
        y = SQUARE_SIZE * self.__row + SQUARE_SIZE / 2
        return y

    def draw(self, window): # Draw the man
        radius = (SQUARE_SIZE / 2) - 10
        if self.__isSelected: # Draw ring to show it is selected -> Draw a larger circle which the man/king is then drawn over (smaller) to appear as a ring around it
            pygame.draw.circle(window, RED, (self.__x, self.__y), (radius+5))
        pygame.draw.circle(window, self.__colour, (self.__x, self.__y), radius)
        if self.__isKing: # Draw crown
            window.blit(CROWN, (self.__x - CROWN.get_width()/2, self.__y - CROWN.get_height()/2))


    def move(self, newRow, newColumn):	
        self.__row = newRow	
        self.__column = newColumn	
        self.__x = self.determineX()	
        self.__y = self.determineY()
